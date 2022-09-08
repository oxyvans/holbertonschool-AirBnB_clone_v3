#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
import json
from flask import request, abort
from models import storage
from models.city import City


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
