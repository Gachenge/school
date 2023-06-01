#!/usr/bin/python3
"""describes a teacher"""
import models
from models.main import Main
from models.main import Base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import relationship
from models.relationship_tables import subject_teacher_association


class Teacher(Main, Base):
    """represents a teacher"""
    if models.store == 'db':
        __tablename__ = 'teachers'
        name = Column(String(128), nullable=False)
        teacher_id = Column(Integer, primary_key=True,  autoincrement=True, default=None)
        email = Column(String(128))
        phone = Column(String(10), nullable=False)
        subjects = relationship("Subject", secondary='subject_teacher_association', back_populates="teacher")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
