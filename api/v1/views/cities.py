#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import request, abort, jsonify
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    if not storage.get(State, state_id):
        abort(404)
    cities_list = []
    for k, v in storage.all(City).items():
        v = v.to_dict()
        if v["state_id"] == state_id:
            cities_list.append(v)
    return jsonify(cities_list)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_cities(state_id):
    if not request.get_json():
        abort(400, 'Not a JSON')
    if not storage.get(State, state_id):
        abort(404)
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    data.update({'state_id': state_id})
    new_city = City(**data)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    obj = storage.get(City, city_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    if not request.get_json():
        abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    ignored_data = ['id', 'state_id', 'created_at', 'updated_at']
    info = request.get_json()
    for k, v in info.items():
        if k not in ignored_data:
            setattr(city, k, v)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
