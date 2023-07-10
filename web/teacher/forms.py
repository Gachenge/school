"""all forms that concern a teacher"""
from flask_login import current_user
from flask_wtf import FlaskForm
from web.models import User
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, Email

class TeacherAccountForm(FlaskForm):
    """gives the teacher access to their account where they can update personal information"""
    name = StringField("Name", validators=[DataRequired(), Length(min=7, max=40)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[DataRequired(), Length(min=10, max=11)])
    submit = SubmitField("Update")

    def validate_username(self, username):
        """check if teacher tries to change their username to an already registered one"""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        """check if teacher tries to change their email to an already registered one"""
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is registered.')
