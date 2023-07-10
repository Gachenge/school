"""this files holds all the forms that belong to the admin"""
import phonenumbers
from web.models import User, Teacher, Student
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, ValidationError
from wtforms import StringField, PasswordField, SubmitField, RadioField

class RegistrationForm(FlaskForm):
    """Registering a new user"""
    fname = StringField("First name", validators=[DataRequired(), Length(min=3, max=20)])
    lname = StringField("Last name", validators=[DataRequired(), Length(min=3, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=7)])
    role = RadioField('Role: ', choices=[('student', 'Student'), ('teacher', 'Teacher'), ('user', 'User'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField("Add")

    def validate_username(self, username):
        """Validate if the username is in the database, throw an error"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        """Validate if the email is registered"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is registered.')
        
class UserUpdateForm(FlaskForm):
    """update a users information"""
    fname = StringField("First name", validators=[DataRequired(), Length(min=3, max=20)])
    lname = StringField("Last name", validators=[DataRequired(), Length(min=3, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    role = RadioField('Role: ', choices=[('student', 'Student'), ('teacher', 'Teacher'), ('user', 'User'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField("Update")

    def validate_username(self, username):
        """if you enter a different  username from the one already in use, check if it is already registered"""
        user = User.query.filter_by(username=username.data).first()
        if user and user.username != username.data:
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        """if you enter a different  email from the one already in use, check if it is already registered"""
        user = User.query.filter_by(email=email.data).first()
        if user and user.email != email.data:
            raise ValidationError('That email is registered.')
        
class TeacherRegistrationForm(FlaskForm):
    """this form is rendered when registering a new teacher"""
    fname = StringField('First name', validators=[DataRequired(), Length(min=3, max=20)])
    lname = StringField("Last name", validators=[DataRequired(), Length(min=3, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[DataRequired(), Length(min=10, max=11)])
    subject = StringField("Subject", validators=[DataRequired()])
    submit = SubmitField("Add teacher")

    def validate_username(self, username):
        """Validate if the username is already registered"""
        user = User.query.filter_by(username=username.data).first()
        if user and user.username != username.data:
            raise ValidationError('That username is taken. Please choose a different one')
        
    def validate_email(self, email):
        """validate if the email is already registered"""
        user = Teacher.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is registered.')

        
class TeacherUpdateForm(FlaskForm):
    """this form is used to update teacher details"""
    fname = StringField('First name', validators=[DataRequired(), Length(min=3, max=20)])
    lname = StringField("Last name", validators=[DataRequired(), Length(min=3, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[DataRequired(), Length(min=10, max=11)])
    subject = StringField("Subject")
    submit = SubmitField("Update teacher")

    def validate_username(self, username):
        """Validate if the username is already registered if a different username is entered"""
        user = User.query.filter_by(username=username.data).first()
        if user and user.username != username.data:
            raise ValidationError('That username is taken. Please choose a different one')
        
    def validate_email(self, email):
        """validate if the email is already registered if a different email is entered"""
        teacher = Teacher.query.filter_by(email=email.data).first()
        if teacher and teacher.email != email.data:
            raise ValidationError('That email is registered.')
        
class StudentRegistrationForm(FlaskForm):
    """register a new student"""
    fname = StringField('First name', validators=[DataRequired(), Length(min=3, max=20)])
    lname = StringField("Last name", validators=[DataRequired(), Length(min=3, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    grade = StringField('Grade', validators=[DataRequired()])
    subject = StringField("Subject", validators=[DataRequired()])
    submit = SubmitField("Add student")

    def validate_username(self, username):
        """Validate if the username is already registered"""
        user = User.query.filter_by(username=username.data).first()
        if user and user.username != username.data:
            raise ValidationError('That username is taken. Please choose a different one')
        
    def validate_email(self, email):
        """validate if the email is already registered"""
        teacher = Teacher.query.filter_by(email=email.data).first()
        if teacher and teacher.email != email.data:
            raise ValidationError('That email is registered.')

class StudentUpdateForm(FlaskForm):
    """render this form to update student details"""
    fname = StringField('First name', validators=[DataRequired(), Length(min=3, max=20)])
    lname = StringField("Last name", validators=[DataRequired(), Length(min=3, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    grade = StringField('Grade')
    subject = StringField("Subject")
    submit = SubmitField("Update student")

    def validate_username(self, username):
        """validate if the username is already registered"""
        user = User.query.filter_by(username=username.data).first()
        if user and user.username != username.data:
            raise ValidationError('That username is taken. Please choose a different one')
        
    def validate_email(self, email):
        """validate if the email is already registered"""
        teacher = Teacher.query.filter_by(email=email.data).first()
        if teacher and teacher.email != email.data:
            raise ValidationError('That email is registered.')

class SubjectRegistrationForm(FlaskForm):
    """register a new subject"""
    name = StringField("Subject name", validators=[DataRequired()])
    tfname = StringField('Teacher first name')
    tlname = StringField("Teacher last name")
    sfname = StringField("Student first name")
    slname = StringField("Student last name")
    grade = StringField("Student's subject grade")
    submit = SubmitField("Add subject")

    def validate_tfname_tlname(self, tfname, tlname):
        """check if the teacher is registered to teach this subject"""
        tname = tfname + ' ' + tlname
        teacher = Teacher.query.filter_by(name=tname).first()
        if not teacher:
            raise ValidationError("Teacher not registered")
        
    def validate_sfname_slname(self, sfname, slname):
        """check if student is registered before adding them to this subject"""
        sname = sfname + ' ' + slname
        student = Student.query.filter_by(name=sname).first()
        if not student:
            raise ValidationError("Student not registered")
