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
from website.forms import UpdateAccountForm, signUp, LoginForm
import secrets
import os
from flask_bcrypt import Bcrypt

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = storage.check_email(form.email.data)
        if user is None:
            flash("Check your email address", 'error')
        elif bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('views.home'))
        else:
            flash("Check password and try again", 'error')
    return render_template("login.html", form=form, user=current_user)

        
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = signUp()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data, password=hashed)
        storage.new(user)
        storage.save()
        flash("Your account has been been created. You can now log in", 'success')
        return redirect(url_for('auth.login'))
    return render_template("signup.html", user=current_user, form=form)
        
            
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
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        storage.save()
        flash("Your account has been updated", 'success')
        return redirect(url_for('auth.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', user=current_user,
                           image_file=image_file, form=form)

