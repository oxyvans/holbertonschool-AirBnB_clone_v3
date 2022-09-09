#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
import json
from flask import request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=('GET', 'POST'))
def cities_state_id(state_id):
    if request.method == 'GET':
        cities_list = []
        for k, v in storage.all(City).items():
            v = v.to_dict()
            if v["state_id"] == state_id:
                cities_list.append(v)
        if cities_list == []:
            abort(404)
        return cities_list

    if request.method == 'POST':
        if storage.get(State, state_id) is None:
            abort(404)
        if request.get_json() is None:
            abort(400, 'Not a JSON')
        data = request.get_json()
        if 'name' not in data.keys():
            abort(400, 'Missing name')
        data.update({'state_id': state_id})
        new_city = City(**data)
        new_city.save()
        return new_city.to_dict(), 201


@app_views.route('/cities/<city_id>', methods=('GET', 'DELETE', 'PUT'))
def cities_city_id(city_id):
    if request.method == 'GET':
        obj = storage.get(City, city_id)
        if obj is None:
            abort(404)

        return obj.to_dict()

    if request.method == 'DELETE':
        obj = storage.get(City, city_id)
        if obj is None:
            abort(404)

        storage.delete(obj)
        storage.save()
        return {}, 200

    if request.method == 'PUT':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        if request.get_json() is None:
            abort(400, 'Not a JSON')
        ignored_data = ['id', 'state_id', 'created_at', 'updated_at']
        for k, v in request.get_json().items():
            if k not in ignored_data:
                setattr(city, k, v)
        city.save()

        return city.to_dict(), 200
