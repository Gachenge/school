from datetime import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from web import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(120), default=None)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(10), nullable=False, default='3456789234')
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), default='user')
    posts = db.relationship('Post', backref='author', cascade='all, delete')

    def get_reset_token(self, expires_sec=1800):
        s =Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s =Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"
    
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable =False)
    phone = db.Column(db.String(10), nullable=False, default='3456789234')
    subjects = db.relationship("Subject", secondary='subject_teacher_association', back_populates="teacher")

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, default='None')
    subjects = db.relationship("Subject", secondary='subject_student_association', back_populates="student")
    grades = db.relationship("SubjectGrade", back_populates="student")

    @property
    def average_grade(self):
        total_grade = sum(int(grade.grade.rstrip('%')) for grade in self.grades)
        grade_count = len(self.grades)
        if grade_count > 0:
            average = total_grade / grade_count
            return "{:.2f}".format(average)
        else:
            return "N/A"


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete="SET NULL"))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete="SET NULL"))
    teacher = db.relationship("Teacher", secondary='subject_teacher_association', back_populates='subjects')
    student = db.relationship('Student', secondary='subject_student_association', back_populates='subjects')
    grades = db.relationship('SubjectGrade', back_populates='subject')


class SubjectGrade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete="SET NULL"))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete="SET NULL"))
    grade = db.Column(db.String(5), nullable=False)

    subject = db.relationship('Subject', back_populates='grades')
    student = db.relationship('Student', back_populates='grades')


subject_teacher_association = db.Table(
    'subject_teacher_association',
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id', ondelete='SET NULL')),
    db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id', ondelete='SET NULL'))
)


subject_student_association = db.Table(
    'subject_student_association',
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id', ondelete='SET NULL')),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id', ondelete='SET NULL'))
)
