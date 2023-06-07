from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models.user import User
from models import storage
from models.teacher import Teacher
from models.student import Student

class UpdateAccountForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


    def validate_email(self, email):
        if email.data != current_user.email:
            users = storage.all(User)
            emails = [user.email for user in users.values()]
            if email.data in emails:
                raise ValidationError('That email is taken. Please choose a different one.')
            

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class requestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request password reset')
    
    def validate_email(self, email):
        users = storage.all(User)
        emails = [user.email for user in users.values()]
        if email.data not in emails:
            raise ValidationError('There is no account associated with that email.')
            
class resetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class signUp(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('first_name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('last_name', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=7)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validateEmail(self, email):
        users = storage.all(User).values()
        if email in [user.email for user in users]:
            raise ValidationError("Email is already registered")
        
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class adteacherForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First name', validators=[DataRequired(), Length(min=3, max=20)])
    last_name = StringField('Lastname', validators=[DataRequired(), Length(min=3, max=20)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=9, max=11)])
    subject = StringField('Subject', validators=[Length(min=3, max=20)])
    submit = SubmitField('Add teacher')

    def validateEmail(self, email):
        teachers = storage.all(Teacher).values()
        if email in [teacher.email for teacher in teachers]:
            raise ValidationError("Email is already registered")

class delteacherForm(FlaskForm):
    first_name = StringField('First name')
    last_name = StringField('Last name')
    teacher_id = StringField('teacher_id')
    submit = SubmitField('Delete teacher')

class upteacherForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First name', validators=[DataRequired(), Length(min=3, max=20)])
    last_name = StringField('Lastname', validators=[DataRequired(), Length(min=3, max=20)])
    teacher_id = StringField('Teacher ID', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=9, max=11)])
    subject = StringField('Subject', validators=[Length(min=3, max=10)])
    submit = SubmitField('Update teacher')

class adstudentForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired(), Length(min=3, max=20)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(min=3, max=20)])
    subject = StringField("Subject name", validators=[DataRequired(), Length(min=3, max=20)])
    grade = StringField("Subject grade", validators=[DataRequired()])
    submit = SubmitField("Add student")

class delstudentForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField("Last name", validators=[DataRequired()])
    student_id = StringField("Student I.D", validators=[DataRequired()])
    submit = SubmitField("Delete student")

class upstudentForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired(), Length(min=3, max=20)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(min=3, max=20)])
    student_id = StringField("Student I.D", validators=[DataRequired()])
    subject = StringField("Subject name", validators=[DataRequired(), Length(min=3, max=20)])
    grade = StringField("Subject grade", validators=[DataRequired()])
    submit = SubmitField("Update student")

class adsubjectForm(FlaskForm):
    name = StringField('Subject name', validators=[DataRequired()])
    tfname = StringField('Subject teacher first name')
    tlname = StringField("Teacher last name")
    sfname = StringField("Student first name")
    slname = StringField("Student last name")
    grade = StringField("Student's subject grade")
    submit = SubmitField("Add subject")

class delsubjectForm(FlaskForm):
    name = StringField('Subject name')
    subject_id = StringField("subject I.D.")
    submit = SubmitField("Delete subject")
