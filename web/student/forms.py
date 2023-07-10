"""contains all the forms that concern a student"""

from flask_login import current_user
from flask_wtf import FlaskForm
from web.models import User, Subject
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Length, Email

class StudentAccountForm(FlaskForm):
    """allows access to every students personal info and allows them to edit some things"""
    fname = StringField("First name", validators=[DataRequired(), Length(min=3, max=20)])
    lname = StringField("Last name", validators=[DataRequired(), Length(min=3, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")

    def validate_username(self, username):
        """do not allow a student to change their username if the new username is already registered"""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        """do not allow a student to change their email if the new email is already registered"""
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is registered.')

class StudentSubjectForm(FlaskForm):
    """allow a student to pick which subjects they take"""
    name = SelectMultipleField("Subjects", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Add") 
