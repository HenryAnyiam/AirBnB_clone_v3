#!/usr/bin/python3
"""module to handle amenities api"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities",
                 strict_slashes=False,
                 methods=['GET', 'POST'])
@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def list_amenities(amenity_id=None):
    """handle amenities data"""
    amenities = storage.all(Amenity).values()
    if amenity_id is not None:
        amenity = [i for i in amenities if i.id == amenity_id]
        if len(amenity) == 0:
            abort(404)
    if request.method == 'GET':
        if amenity_id is None:
            amenity_list = [i.to_dict() for i in amenities]
            return jsonify(amenity_list)
        return jsonify(amenity[0].to_dict())
    elif request.method == 'POST':
        value = request.get_json()
        if value is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        else:
            if 'name' not in value:
                return make_response(jsonify({'error': 'Missing name'}), 400)
            amenity = Amenity(**value)
            amenity.save()
            return make_response(jsonify(amenity.to_dict()), 201)
    elif request.method == 'DELETE':
        storage.delete(amenity[0])
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        value = request.get_json()
        if value is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        else:
            ignore = ['id', 'created_at', 'updated_at']
            for i in value:
                if i not in ignore:
                    setattr(amenity[0], i, value.get(i))
                    storage.save()
            return make_response(jsonify(amenity[0].to_dict()), 200)
