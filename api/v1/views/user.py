#!/usr/bin/python3

from flask import Flask
from flask import jsonify
from flask import make_response
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import request
from flask import abort

@app_views.route("/users", methods=['GET', 'POST'],
                 strict_slashes=False)
def creuser():
    if request.method == 'GET':
        objects = [obj.to_dict() for obj in storage.all(User).values()]
        return jsonify(objects)
    elif request.method == 'POST':
        if not request.get_json():
            abort(404)
        req = request.get_json()
        if 'email' not in req:
            return make_response(jsonify({"error": "Missing Email"}), 400)
        if 'password' not in req:
            return make_response(jsonify({"error": "Missing password"}), 400)
        if 'first_name' not in req:
            return make_response(jsonify({"error": "Missing first name"}), 400)
        if 'last_name' not in req:
            return make_response(jsonify({"error": "Missing last name"}), 400)
        new = User(**req)
        new.save()
        return jsonify(new.to_dict()), 201
    
@app_views.route("/users/<user_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def geuser(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        user.delete()
        storage.save()
        return jsonify({})
    elif request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, value)
        return jsonify(user.to_dict())
