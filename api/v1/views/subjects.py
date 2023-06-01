#!/usr/bin/python3

from flask import Flask
from flask import jsonify
from flask import make_response
from models import storage
from models.subjects import Subject
from api.v1.views import app_views
from flask import request
from flask import abort

@app_views.route("/subjects", methods=['GET', 'POST'],
                 strict_slashes=False)
def subs():
    if request.method == 'GET':
        objects = [obj.to_dict() for obj in storage.all(Subject).values()]
        return jsonify(objects)
    elif request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        if 'name' not in req:
            return make_response(jsonify({"error": "Missing name"}), 400)
        if 'student_id' not in req:
            return make_response(jsonify({"error": "Missing student id"}), 400)
        if 'teacher_id' not in req:
            return make_response(jsonify({"error": "Missing teacher id"}), 400)
        new = Subject(**req)
        new.save()
        return jsonify(new.to_dict()), 201
    
@app_views.route("/subjects/<subject_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def subsi(subject_id):
    subject = storage.get(Subject, subject_id)
    if subject is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(subject.to_dict())
    elif request.method == 'DELETE':
        subject.delete()
        storage.save()
        return jsonify({})
    elif request.method == 'PUT':
        req = request.get_json()
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        for key, value in req.items():
            if key not in ['id', 'updated_at', 'created_at']:
                setattr(subject, key, value)
        return jsonify(subject.to_dict())
