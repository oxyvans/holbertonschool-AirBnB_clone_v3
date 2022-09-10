#!/usr/bin/python3
""" task 10 """

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ all users """
    all_u = storage.all(User).values()
    users = []
    for u in all_u:
        users.append(u.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def user_by_id(user_id):
    """ user by id """
    u = storage.get(User, user_id)
    if u:
        return jsonify(u.to_dict())
    abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def deletear_u(user_id):
    """ deletes """
    u = storage.get(User, user_id)
    if not u:
        abort(404)
    storage.delete(u)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_u():
    """ creates """
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'email' not in request.get_json():
        abort(400, "Missing email")
    if 'password' not in request.get_json():
        abort(400, "Missing password")
    u = User(**request.get_json())
    u.save()
    return make_response(jsonify(u.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_u(user_id):
    """ updates """
    if not request.get_json():
        abort(400, "Not a JSON")
    ignored = ['id', 'email', 'created_at', 'updated_at']
    u = storage.get(User, user_id)
    if not u:
        abort(404)
    info = request.get_json()
    for key, value in info.items():
        if key not in ignored:
            setattr(u, key, value)
    storage.save()
    return make_response(jsonify(u.to_dict()), 200)
