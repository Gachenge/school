#!/usr/bin/python3

"""handles login and other accounts"""
import models
from models.main import Main
from models.main import Base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship
from hashlib import md5
from flask_login import UserMixin


class User(Main, UserMixin, Base):
    if models.store == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False, unique=True)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
