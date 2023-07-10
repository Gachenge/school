"""contains all routes connected to the user"""

from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message
from web.models import User, Post
from web.users.forms import RegistratrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from web.users.utils import save_picture
from web import bcrypt, db, mail

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    """register/signupo as a new user"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistratrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.fname.data+' '+form.lname.data, username=form.username.data, email=form.email.data, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    """registered users can login here"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login failed. Check email and password", "danger")
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    """allow for user logout"""
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """access your personal details and allow for updating"""
    form =UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.fname.data+' '+form.lname.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        if current_user.name:
            form.fname.data, form.lname.data = current_user.name.split(' ')
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title='Account', image_file=image_file, form=form)

@users.route("/user/<string:username>")
@login_required
def user_posts(username):
    """access all posts added by a particular user"""
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=2)
    return render_template('user_posts.html', posts=posts, user=user)

def send_reset_email(user):
    """if user forgets their password, send a reset token to the email address supplied"""
    token = user.get_reset_token()
    msg = Message("Password Reset Request", sender='noreply@demo.com', recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this message.
"""
    mail.send(msg)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """allow a user to request a password reset request"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent to your Email to reset your password", 'info')
        return redirect(url_for('users.login'))
    return render_template("reset_request.html", title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """verify the reset token and allow for password reset if valid"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed
        db.session.commit()
        flash(f"Yor password has been updated.You are now able to log in!", 'success')
        return redirect(url_for('users.login'))
    return render_template("reset_token.html", title='Reset Password', form=form)

