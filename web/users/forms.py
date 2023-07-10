"""handles users. signup and login"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from flask_login import current_user
from web.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistratrationForm(FlaskForm):
    """renders the user signup form"""
    fname = StringField("First name", validators=[DataRequired(), Length(min=3, max=20)])
    lname = StringField("Last name", validators=[DataRequired(), Length(min=3, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=7)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        """ensure only a new username can be registered"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        """ensure only a new email is registered"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is registered.')


class LoginForm(FlaskForm):
    """render the login form"""
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=7)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log in")


class UpdateAccountForm(FlaskForm):
    """allow users to update their personal information and add a new profile picture"""
    fname = StringField("First name", validators=[DataRequired(), Length(min=3, max=20)])
    lname = StringField("Last name", validators=[DataRequired(), Length(min=3, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField("Update profile picture", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        """do not allow username to be an already registered one"""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        """email may not be already registered by someone else"""
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is registered.')
            
class RequestResetForm(FlaskForm):
    """in case a user forgets their password"""
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password filed')

    def validate_email(self, email):
        """check if the email supplied to reset password is registered"""
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('That email is  not registered. Sign up first')
        
class ResetPasswordForm(FlaskForm):
    """reset user password form"""
    password = PasswordField("Password", validators=[DataRequired(), Length(min=7)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password filed')