#!/usr/bin/python3
"""define all users of the school"""
from uuid import uuid4
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
import pytz
from os import getenv

eat_time = pytz.timezone("Africa/Nairobi")

time = "%Y-%m-%dT%H:%M:%S.%f"

if models.store == 'db':
    Base = declarative_base()
else:
    Base = object


class Main:
    """define all other users"""

    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now(eat_time))
    updated_at = Column(DateTime, nullable=False, default=datetime.now(eat_time))

    def __init__(self, *args, **kwargs):
        """initialise all attributes"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid4())
        else:
            self.id = str(uuid4())
            self.created_at = self.updated_at = datetime.utcnow()

    def __str__(self):
        """string representation"""
        return "[{}] ({}) {}".format(type(self).__name__, self.id,
                                     self.__dict__.copy())

    def save(self):
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, saves=None):
        """returns a dictionary of all key value instances"""
        new_dict = self.__dict__.copy()
        if 'created_at' in new_dict:
            new_dict['created_at'] = new_dict['created_at'].strftime("%Y-%m-%dT%H:%M:%S.%f")
        if 'updated_at' in new_dict:
            new_dict['updated_at'] = new_dict['updated_at'].strftime("%Y-%m-%dT%H:%M:%S.%f")
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if saves is None:
            if "password" in new_dict:
                del new_dict["password"]
        return new_dict

    def delete(self):
        models.storage.delete(self)
