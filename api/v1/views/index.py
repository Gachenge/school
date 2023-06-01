#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.student import Student
from models.subjects import Subject
from models.teacher import Teacher
from models.user import User

@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    return jsonify({"status": "OK"})

@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def count():
    counts = {
        "Users": storage.count(User),
        "Teachers": storage.count(Teacher),
        "Students": storage.count(Student),
        "Subjects": storage.count(Subject) 
    }
    return jsonify(counts)
