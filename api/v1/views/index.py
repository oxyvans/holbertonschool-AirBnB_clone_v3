#!/usr/bin/python3
"""initialize index"""
from api.v1.views import app_views


@app_views('/status')
def show():
    return json.dumps({"status": "OK"})
