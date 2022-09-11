#!/usr/bin/python3
"""view for Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    if not storage.get(Place, place_id):
        abort(404)
    review_list = []
    for k, v in storage.all(Review).items():
        v = v.to_dict()
        if v["place_id"] == place_id:
            review_list.append(v)
    return jsonify(review_list)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_reviews(place_id):
    if not request.get_json():
        abort(400, 'Not a JSON')
    if not storage.get(Place, place_id):
        abort(404)
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if not storage.get(User, data['user_id']):
        abort(404)
    if 'text' not in data:
        abort(400, 'Missing text')
    data.update({'place_id': place_id})
    new_review = Review(**data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    obj = storage.get(Review, review_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    if not request.get_json():
        abort(400, 'Not a JSON')
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    ignored_data = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    info = request.get_json()
    for k, v in info.items():
        if k not in ignored_data:
            setattr(review, k, v)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
