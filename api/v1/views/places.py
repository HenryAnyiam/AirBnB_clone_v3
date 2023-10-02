#!/usr/bin/python3
"""module to handle places api"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.users import User


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def list_place(city_id=None):
    """list places according to city id"""
    if city_id is None:
        abort(404)
    cities = storage.all(City).values()
    city = [i for i in cities if i.id == city_id]
    if len(city) == 0:
        abort(404)
    places = storage.all(Place).values()
    place = [i for i in places if i.city_id == city_id]
    if request.method == 'GET':
        list_place = [i for i in places if i.city_id == city_id]
        return jsonify(list_place)
    elif request.method == 'POST':
        try:
            values = request.get_json()
        except Exception:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        else:
            if 'name' not in values:
                return make_response(jsonify({'error': 'Missing name'}), 400)
            if 'user_id' not in values:
                val = jsonify({'error': 'Missing user_id'})
                return make_response(val, 400)
            users = storage.all(User).values()
            user = [i for i in users if i.user_id == values['user_id']]
            if len(user) == 0:
                abort(403)
            values['city_id'] = city_id
            place = Place(**values)
            place.save()
            return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>",
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def find_place(place_id=None):
    """find place with id"""
    if place_id is None:
        abort(404)
    places = storage.all(Place).values()
    place = [i for i in places if i.id == place_id]
    if len(place) == 0:
        abort(404)
    if request.method == 'GET':
        return jsonify(place[0].to_dict())
    elif request.method == 'PUT':
        ignore = ['id', 'user_id','city_id', 'created_at', 'updated_at']
        try:
            values = request.get_json()
        except Exception:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        else:
            for i in values:
                if i not in ignore:
                    setattr(place[0], i, values.get(i))
                    storage.save()
            return make_response(jsonify(place[0].to_dict()), 200)
    elif request.method == 'DELETE':
        storage.delete(place[0])
        storage.save()
        return make_response(jsonify({}), 200)
