#!/usr/bin/python3
""" task 9 """

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """ all amenities """
    all_a = storage.all(Amenity).values()
    Amenitys = []
    for a in all_a:
        Amenitys.append(a.to_dict())
    return jsonify(Amenitys)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amen_by_id(amenity_id):
    """ amen by id """
    a = storage.get(Amenity, amenity_id)
    if a:
        return jsonify(a.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def deletear_a(amenity_id):
    """ deletes """
    a = storage.get(Amenity, amenity_id)
    if not a:
        abort(404)
    storage.delete(a)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_a():
    """ creates """
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    a = Amenity(**request.get_json())
    a.save()
    return make_response(jsonify(a.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def update_a(amenity_id):
    """ updates """
    if not request.get_json():
        abort(400, "Not a JSON")
    ignored = ['id', 'created_at', 'updated_at']
    a = storage.get(Amenity, amenity_id)
    if not a:
        abort(404)
    info = request.get_json()
    for key, value in info.items():
        if key not in ignored:
            setattr(a, key, value)
    storage.save()
    return make_response(jsonify(a.to_dict()), 200)
