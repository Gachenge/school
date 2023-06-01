#!/usr/bin/python3

from models import storage
from models.student import Student
from api.v1.views import app_views
from flask import jsonify
from flask import make_response
from flask import request
from flask import abort

@app_views.route("/students", methods=['GET', 'POST'], strict_slashes=False)
def gestud():
    if request.method == 'GET':
        stud = [obj.to_dict() for obj in storage.all(Student).values()]
        return jsonify(stud)
    elif request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if 'name' not in request.get_json():
            return make_response(jsonify({"error": "Missing name"}), 400)
        if 'average_grade' not in request.get_json():
            return make_response(jsonify({"error": "Missing average grade"}), 400)
        stude = request.get_json()
        new = Student(**stude)
        new.save()
        return jsonify(new.to_dict()), 201
    
@app_views.route("/students/<student_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def getstudent(student_id):
    student = storage.get(Student, student_id)
    if student is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(student.to_dict())
    elif request.method == 'DELETE':
        student.delete()
        storage.save()
        return jsonify({})
    elif request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(student, key, value)
        return jsonify(student.to_dict())
