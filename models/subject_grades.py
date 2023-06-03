#!/usr/bin/python3

import models
from models.main import Base
from models.main import Main
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship

class SubjectGrade(Main, Base):
    __tablename__ = 'subject_grades'
    subject_grade_id = Column(Integer, primary_key=True, autoincrement=True)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id', ondelete="SET NULL"))
    student_id = Column(Integer, ForeignKey('students.student_id', ondelete="SET NULL"))
    grade = Column(String(5), nullable=False)

    subject = relationship('Subject', back_populates='grades')
    student = relationship('Student', back_populates='grades')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
