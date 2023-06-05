#!/usr/bin/python3
"""handles storage in database"""
from sqlalchemy import create_engine
from os import getenv
from models.main import Main
from models.main import Base
from models.student import Student
from models.teacher import Teacher
from models.subjects import Subject
from models.user import User
from models.subject_grades import SubjectGrade
from models.blog import Blog
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from hashlib import md5
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from models.relationship_tables import subject_student_association

classes = {"User": User, "Student": Student, "Main": Main, "Blog": Blog,
           "Teacher": Teacher, "Subject": Subject, "SubjectGrade": SubjectGrade}


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("user"),
                                             getenv("password"),
                                             getenv("host"),
                                             getenv("database")))

    def all(self, cls=None):
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        self.__session.close()

    def get(self, cls, id):
        try:
            obj = self.all(cls)
            for ob in obj.values():
                if ob.id == id:
                    return ob
        except Exception:
            return None

    def count(self, cls=None):
        if not cls:
            count = 0
            for cl in classes.values():
                count += len(self.storage.all(cl).values())
        else:
            count = len(self.all(cls).values())
        return count
    
    def rollback(self):
        try:
            self.__session.rollback()
        except SQLAlchemyError as e:
            print("Rollback error: {}".function(str(e)))
    
    def authenticate_user(self, email, password):
        try:
            admins = []
            user = self.__session.query(User).filter_by(email=email).first()
            hashed = md5(password.encode()).hexdigest()
            if user and hashed == user.password:
                return user
            else:
                return None
        except Exception as e:
            self.rollback()
            print(f"Authentication error: {str(e)}")
            return None
        
    def check_email(self, email):
        user = self.__session.query(User).filter_by(email=email).first()
        return user
    
    def get_user_by_id(self, user_id):
        try:
            user = self.__session.query(User).get(user_id)
            return user
        except Exception as e:
            self.rollback()
            print(f"Error retrieving user: {str(e)}")
            return None
        
    def get_subjects(self):
        try:
            subjects = self.__session.query(Subject).options(joinedload(Subject.students)).all()
            return subjects
        except Exception as e:
            self.rollback()
            return []

    def get_average(self, student):
        if isinstance(student, Student):
            if student.subjects:
                total_grades = 0
                for subject in student.subjects:
                    grade = self.get_grade(subject.subject_id, student.student_id)
                    if grade is not None:
                        total_grades += grade
                if total_grades > 0:
                    average = total_grades / len(student.subjects)
                    student.average_grade = str(average)
                else:
                    student.average_grade = "N/A"
                self.new(student)
                self.save()
            else:
                student.average_grade = "N/A"
        else:
            raise ValueError("Invalid student object provided")
        
    def get_grade(self, subject_id, student_id):
        grade = None
        try:
            grade = self.__session.query(SubjectGrade.grade).filter(
                SubjectGrade.subject_id == subject_id,
                SubjectGrade.student_id == student_id
            ).scalar()
        except Exception as e:
            self.rollback()
            print(f"Error retrieving student grade: {str(e)}")
        return grade
