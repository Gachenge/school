#!/usr/bin/python3

from flask import Flask
from flask import jsonify
from flask import make_response
from models import storage
from models.teacher import Teacher
from api.v1.views import app_views
from flask import request
from flask import abort

@app_views.route("/teachers", methods=['GET', 'POST'])
def geteach():
    if request.method == 'GET':
        objects = [obj.to_dict() for obj in storage.all(Teacher).values()]
        return jsonify(objects)
    elif request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        if 'name' not in req:
            return make_response(jsonify({"error": "Missing name"}), 400)
        if 'phone' not in req:
            return make_response(jsonify({"error": "Missing phone"}), 400)
        new = Teacher(**req)
        new.save()
        return jsonify(new.to_dict())

@app_views.route("/teachers/<teacher_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def teach(teacher_id):
    teacher = storage.get(Teacher, teacher_id)
    if teacher is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(teacher.to_dict())
    elif request.method == 'DELETE':
        teacher.delete()
        storage.save()
        return jsonify({})
    elif request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        for key, value in req.items():
            if key not in ['id', 'updated_at', 'created_at']:
                setattr(teacher, key, value)
        return jsonify(teacher.to_dict())
