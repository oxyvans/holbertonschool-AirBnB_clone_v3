#!/usr/bin/python3
"""initialize index"""
from api.v1.views import app_views
from models import storage
import json


@app_views.route('/status')
def show():
    return ({"status": "OK"})


@app_views.route('/stats')
def stats():
    classes = {"amenities": "Amenity", "cities": "City", "places": "Place",
               "reviews": "Review", "states": "State", "users": "User"}
    classes_count = {}
    for k, v in classes.items():
        classes_count.update({k: storage.count(v)})
    return classes_count
