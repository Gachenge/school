import phonenumbers
from web.models import User, Teacher, Student
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, ValidationError
from wtforms import StringField, PasswordField, SubmitField, RadioField

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=7)])
    role = RadioField('Role: ', choices=[('student', 'Student'), ('user', 'User'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField("Add")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is registered.')
        
class UserUpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    role = RadioField('Role: ', choices=[('student', 'Student'), ('user', 'User'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField("Update")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and user.username != username.data:
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and user.email != email.data:
            raise ValidationError('That email is registered.')
        
class TeacherRegistrationForm(FlaskForm):
    fname = StringField('First name', validators=[DataRequired(), Length(min=3, max=20)])
    lname = StringField("Last name", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[DataRequired(), Length(min=10, max=11)])
    subject = StringField("Subject", validators=[DataRequired()])
    submit = SubmitField("Add teacher")
        
    def validate_email(self, email):
        user = Teacher.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is registered.')

        
class TeacherUpdateForm(FlaskForm):
    fname = StringField('First name', validators=[DataRequired(), Length(min=3, max=20)])
    lname = StringField("Last name", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[DataRequired(), Length(min=10, max=11)])
    subject = StringField("Subject")
    submit = SubmitField("Update teacher")
        
    def validate_email(self, email):
        teacher = Teacher.query.filter_by(email=email.data).first()
        if teacher and teacher.email != email.data:
            raise ValidationError('That email is registered.')
        
class StudentRegistrationForm(FlaskForm):
    fname = StringField('First name', validators=[DataRequired(), Length(min=3, max=20)])
    lname = StringField("Last name", validators=[DataRequired(), Length(min=3, max=20)])
    grade = StringField('Grade', validators=[DataRequired()])
    subject = StringField("Subject", validators=[DataRequired()])
    submit = SubmitField("Add student")

class StudentUpdateForm(FlaskForm):
    fname = StringField('First name', validators=[DataRequired(), Length(min=3, max=20)])
    lname = StringField("Last name", validators=[DataRequired(), Length(min=3, max=20)])
    grade = StringField('Grade')
    subject = StringField("Subject")
    submit = SubmitField("Update student")

class SubjectRegistrationForm(FlaskForm):
    name = StringField("Subject name", validators=[DataRequired()])
    tfname = StringField('Teacher first name')
    tlname = StringField("Teacher last name")
    sfname = StringField("Student first name")
    slname = StringField("Student last name")
    grade = StringField("Student's subject grade")
    submit = SubmitField("Add subject")

    def validate_tfname_tlname(self, tfname, tlname):
        tname = tfname + ' ' + tlname
        teacher = Teacher.query.filter_by(name=tname).first()
        if not teacher:
            raise ValidationError("Teacher not registered")
        
    def validate_sfname_slname(self, sfname, slname):
        sname = sfname + ' ' + slname
        student = Student.query.filter_by(name=sname).first()
        if not student:
            raise ValidationError("Student not registered")
