#!/usr/bin/python3

import models
from models.main import Main
from models.main import Base
from models.teacher import Teacher
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models.relationship_tables import subject_student_association
from models.relationship_tables import subject_teacher_association


class Subject(Main, Base):
    if models.store == 'db':
        __tablename__ = 'subjects'
        name = Column(String(128), nullable=False)
        subject_id = Column(Integer, primary_key=True, autoincrement=True,
                            default=None)
        teacher_id = Column(Integer, ForeignKey('teachers.teacher_id', ondelete='SET NULL'))
        student_id = Column(Integer, ForeignKey('students.student_id', ondelete='SET NULL'))
        teacher = relationship('Teacher', secondary='subject_teacher_association', back_populates='subjects')
        student = relationship('Student', secondary='subject_student_association', back_populates='subjects')
        grades = relationship('SubjectGrade', back_populates='subject')
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
