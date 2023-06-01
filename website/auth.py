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
                return redirect(url_for('views.home'))
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
