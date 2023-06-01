#!/usr/bin/python3
from os import getenv

"""storage"""
store = getenv("type_storage")

if store == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
