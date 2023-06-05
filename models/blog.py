#!/usr/bin/python3

import models
from models.main import Base
from models.main import Main
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import TEXT
from sqlalchemy.orm import relationship

class Blog(Main, Base):
    if models.store == 'db':
        __tablename__ = 'blog'
        blog_id = Column(Integer, primary_key=True,  autoincrement=True, default=None)
        title = Column(String(100), nullable=False)
        content = Column(TEXT, nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.Main.created_at})"
