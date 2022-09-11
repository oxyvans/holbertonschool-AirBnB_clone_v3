#!/usr/bin/python3
"""view for Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    if not storage.get(City, city_id):
        abort(404)
    places_list = []
    for k, v in storage.all(Place).items():
        v = v.to_dict()
        if v["city_id"] == city_id:
            places_list.append(v)
    return jsonify(places_list)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_places(city_id):
    if not request.get_json():
        abort(400, 'Not a JSON')
    if not storage.get(City, city_id):
        abort(404)
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if not storage.get(User, data['user_id']):
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    data.update({'city_id': city_id})
    new_place = Place(**data)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    obj = storage.get(Place, place_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    if not request.get_json():
        abort(400, 'Not a JSON')
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    ignored_data = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    info = request.get_json()
    for k, v in info.items():
        if k not in ignored_data:
            setattr(place, k, v)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    states, cities, amenities = [], [], []
    if 'states' in data.keys():
        states = data['states']
    if 'cities' in data.keys():
        cities = data['cities']
    if 'amenities' in data.keys():
        amenities = data['amenities']
    cities_list = []
    if cities == [] and states == []:
        for k, v in storage.all(City).items():
            cities_list.append(v.to_dict())
    for state in states:
        for k, v in storage.all(City).items():
            v = v.to_dict()
            if v["state_id"] == state_id:
                cities_list.append(v)
    for city in cities:
        obj = storage.get(City, city)
        if obj and obj.to_dict() not in cities_list:
            cities_list.append(obj.to_dict())
    places_list = []
    for cty in cities_list:
        for k, v in storage.all(Place).items():
            v = v.to_dict()
            if amenities == []:
                places_list.append(v)
            if v["city_id"] == cty['id'] and v['state_id'] == cty['state_id']:
                for i in amenities:
                    if i not in v['amenities']:
                        continue
                places_list.append(v)
    return jsonify(places_list)
