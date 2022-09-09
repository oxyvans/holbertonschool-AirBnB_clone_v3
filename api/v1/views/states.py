#!/usr/bin/python3
""" task 7 """

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ all states """
    all_s = storage.all(State).values()
    States = []
    for s in all_s:
        States.append(s.to_dict())
    return jsonify(States)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_by_id(state_id):
    """ state by id """
    s = storage.get(State, state_id)
    if s:
        return jsonify(s.to_dict())
    abort(404)

@app_views.route('states/<state_id>', methods=['DELETE'], strict_slashes=False)
def deletear(state_id):
    """ deletes """
    s = storage.get(State, state_id)
    if not s:
        abort(404)
    storage.delete(s)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create():
    """ creates """
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    s = State(**request.get_json())
    s.save()
    return make_response(jsonify(s.to_dict()), 201)

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update(state_id):
    """ updates """
    if not request.get_json():
        abort(400, "Not a JSON")
    ignored = ['id', 'created_at', 'updated_at']
    s = storage.get(State, state_id)
    if not s:
        abort(404)
    info = request.get_json()
    for key, value in info.items():
        if key not in ignored:
            setattr(s, key, value)
    storage.save()
    return make_response(jsonify(s.to_dict()), 200)
