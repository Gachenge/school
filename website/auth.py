from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from models import storage
from models.user import User
from flask import redirect
from flask import url_for
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user
from website.forms import UpdateAccountForm
import secrets
import os


auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = storage.check_email(email)
        if user:
            if storage.authenticate_user(email, password):
                flash("Login successful", category='success')
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('views.home'))
            else:
                flash("Incorect password, try again", category='error')
        else:
            flash("Email does not exist", category='error')
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        details = {
            'email': request.form.get('email'),
            'first_name': request.form.get('firstName'),
            'last_name': request.form.get('lastName'),
            'password': request.form.get('password1'),
            'password2': request.form.get('password2')
        }
        if storage.check_email(details.get('email')):
            flash("Email is already registered", category='error')               
        elif len(details['email']) < 6:
            flash("Enter a valid E-Mail.", category='error')
        elif len(details['first_name']) < 3:
            flash("First name must be greater than 2 characters", category='error')
        elif len(details['last_name']) < 3:
            flash("Last name must be greater than 2 characters", category='error')
        elif (details['password']) != (details['password2']):
            flash("Passwords do not match", category='error')
        elif len(details['password']) < 7:
            flash("password must be at least 7 characters long", category='error')
        else:
            user = User(**details)
            storage.new(user)
            storage.save()
            login_user(user, remember=True)
            flash("Account created!", category='success')
            return redirect(url_for('views.home'))
    return render_template("signup.html", user=current_user)

@auth.route('/admin')
@login_required
def admin():
    if current_user.role == 'admin':
        return render_template("admin.html", user=current_user)
    else:
        flash("You do not have enough permissions to access this page", category='error')
        return redirect(url_for('views.home'))
    
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(auth.root_path, 'static/images', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@auth.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.email = form.email.data
        storage.save()
        flash("Your account has been updated", 'success')
        return redirect(url_for('auth.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', user=current_user,
                           image_file=image_file, form=form)

