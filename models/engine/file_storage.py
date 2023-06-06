#!/usr/bin/python3
"""handle storage in a file"""

import json
from models.main import Main
from models.student import Student
from models.teacher import Teacher
from models.subjects import Subject
from models.main import Base
from models.user import User
from models.subject_grades import SubjectGrade
from models.blog import Blog
from hashlib import md5
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from models.relationship_tables import subject_student_association
from flask_sqlalchemy import Pagination

classes = {"User": User, "Student": Student, "Main": Main, "Blog": Blog,
           "Teacher": Teacher, "Subject": Subject, "SubjectGrade": SubjectGrade}


class FileStorage:
    __file_path = "school.json"
    __objects = {}

    def all(self, cls=None):
        """returns a dictionary of all objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            self.__objects[key] = obj

    def save(self):
        """serialises __objects to json file"""
        json_objects = {}
        for key in self.__objects:
            if key == "password":
                json_objects[key].decode()
            json_objects[key] = self.__objects[key].to_dict(saves=1)
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserialise the json file into a python object"""
        try:
            with open(self.__file_path, 'r') as f:
                objdict = json.load(f)
                for val in objdict.values():
                    name = val["__class__"]
                    del val["__class__"]
                    self.new(eval(name)(**val))
        except FileNotFoundError:
            return

    def delete(self, obj=None):
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        self.reload()

    def get(self, cls, id):
        try:
            obj = self.all(cls)
            for ob in obj.values():
                if ob.id == id:
                    return ob
        except Exception as e:
            print(e)

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
            user = self.__session.query(User).filter_by(email=email).first()
            hashed = md5(user.password.encode()).hexdigest()
            if user and user.password == password:
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
            user = self.__session.query(User).get(int(user_id))
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

    def paginate(self, cls, page):
        try:
            query = self.__session.query(cls)
            per_page = 1
            posts = query.paginate(page, per_page)
        except Exception as e:
            self.rollback()
            print("Error paginating:", str(e))
            return None

        return posts