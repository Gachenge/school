#!/usr/bin/python3

"""handles login and other accounts"""
import models
from models.main import Main
from models.main import Base
from models.blog import Blog
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer


class User(Main, UserMixin, Base):
    if models.store == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False, unique=True)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        image_file = Column(String(20), nullable=False, default='default.png')
        role = Column(String(20), nullable=False, default='user')
        posts = relationship('Blog', backref='author', lazy=True)
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return models.storage.get(User, user_id)
