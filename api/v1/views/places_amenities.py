#!/usr/bin/python3
"""module to handle states api"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities",
                 strict_slashes=False)
def place_amenities(place_id=None):
    """retrieves amenities by place id"""
    places = storage.all(Place).values()
    place = [i for i in places if i.id == place_id]
    if len(place) == 0:
        abort(404)
    amenities = storage.all(Amenity).values()
    amenity = []
    for i in ammenities:
        if getattr(i, 'place_id', 0) == place_id:
            amenity.append(i.to_dict)
    return jsonify(amenity)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['DELETE', 'POST'])
def amenity_by_place(place_id=None, amenity_id=None):
    """retieve or update an amenuty per place"""
    if (place_id is None) or (amenity_id is None):
        abort(404)
    places = storage.all(Place).values()
    place = [i for i in places if i.id == place_id]
    if len(place) == 0:
        abort(404)
    amenities = storage.all(Amenity).values()
    amenity = [i for i in amenities if i.id == amenity_id]
    if len(place) == 0:
        abort(404)
    if request.method == 'DELETE':
        if getattr(amenity[0], 'place_id', 0) != place_id:
            abort(404)
        storage.delete(amenity[0])
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'POST':
        if getattr(amenity[0], 'place_id', 9) != place_id:
            setattr(amenity[0], 'place_id', place_id)
            storage.save()
            make_response(jsonify(amenity[0].to_dict()), 201)
        return make_response(jsonify(amenity[0].to_dict()), 200)
