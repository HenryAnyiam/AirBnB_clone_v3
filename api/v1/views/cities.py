#!/usr/bin/python3
"""module to handle citiess api"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def list_city(state_id=None):
    """list cities according to state id"""
    if state_id is None:
        abort(404)
    states = storage.all(State).values()
    state = [i for i in states if i.id == state_id]
    if len(state) == 0:
        abort(404)
    if request.method == 'GET':
        cities = []
        for city in state[0].cities:
            cities.append(city.to_dict())
        return jsonify(cities)
    elif request.method == 'POST':
        try:
            values = request.get_json()
        except Exception:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        else:
            if 'name' not in values:
                return make_response(jsonify({'error': 'Missing name'}), 400)
            city = City(state_id=state_id, name=values.get('name'))
            city.save()
            return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>",
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def find_city(city_id=None):
    """find city with id"""
    if city_id is None:
        abort(404)
    cities = storage.all(City).values()
    city = [i for i in cities if i.id == city_id]
    if len(city) == 0:
        abort(404)
    if request.method == 'GET':
        return jsonify(city[0].to_dict())
    elif request.method == 'PUT':
        ignore = ['id', 'state_id', 'created_at', 'updated_at']
        try:
            values = request.get_json()
        except Exception:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        else:
            for i in values:
                if i not in ignore:
                    setattr(city[0], i, values.get(i))
                    storage.save()
            return make_response(jsonify(city[0].to_dict()), 200)
    elif request.method == 'DELETE':
        storage.delete(city[0])
        storage.save()
        return make_response(jsonify({}), 200)
