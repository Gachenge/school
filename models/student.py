#!/usr/bin/python3
"""represents a student"""

import models
from models.main import Main
from models.main import Base
from models.subjects import Subject
from models.subject_grades import SubjectGrade
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Integer
from models.relationship_tables import subject_student_association

class Student(Main, Base):
    if models.store == 'db':
        __tablename__ = 'students'
        name = Column(String(128), nullable=False)
        student_id = Column(Integer, autoincrement=True, primary_key=True)
        subjects = relationship("Subject", secondary='subject_student_association', back_populates="student")
        grades = relationship("SubjectGrade", back_populates="student")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def average_grade(self):
        total_grade = sum(int(grade.grade.rstrip('%')) for grade in self.grades)
        grade_count = len(self.grades)
        if grade_count > 0:
            average = total_grade / grade_count
            return "{:.2f}".format(average)
        else:
            return "N/A"

