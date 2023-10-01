#!/usr/bin/python3
"""index file for blueprint"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def index():
    """returns a 200 JSON status"""
    return jsonify({"starus": "OK"})
