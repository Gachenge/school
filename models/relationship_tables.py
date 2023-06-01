#!/usr/bin/python3

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from models.main import Base

subject_teacher_association = Table(
    'subject_teacher_association',
    Base.metadata,
    Column('subject_id', Integer, ForeignKey('subjects.subject_id', ondelete='SET NULL')),
    Column('teacher_id', Integer, ForeignKey('teachers.teacher_id', ondelete='SET NULL'))
)

subject_student_association = Table(
    'subject_student_association',
    Base.metadata,
    Column('subject_id', Integer, ForeignKey('subjects.subject_id')),
    Column('student_id', Integer, ForeignKey('students.student_id'))
)
