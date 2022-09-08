#!/usr/bin/python3
"""initialize index"""
from api.v1.views import app_views
import json


@app_views.route('/status')
def show():
    return ({"status": "OK"})
