#!/usr/bin/python3
"""module to handle states api"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/states",
                 strict_slashes=False,
                 methods=['GET', 'POST'])
@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def list_states(state_id=None):
    """handles methods for the State class"""
    all_states = storage.all(State)
    """handle GET method"""
    if request.method == 'GET':
        if state_id is None:
            values = all_states.values()
            states = [i.to_dict() for i in values]
            return jsonify(states)
        state = [i.to_dict() for i in values if i.id == state_id]
        if len(state) == 0:
            abort(404)
        return jsonify(state[0])
    elif request.method == 'POST':
        """Handle POST method to create a new State instance"""
        try:
            value = request.get_json()
        except Exception:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        else:
            if 'name' in value:
                state = State(name=value.get('name'))
                state.save()
                return make_response(jsonify(state.to_dict()), 201)
            else:
                return make_response(jsonify({'error': 'Missing name'}), 400)
    elif (request.method == 'DELETE') or (request.method == 'PUT'):
        """Handle DELETE method to delete a State instance
        Also handles PUT method, to update a class instance"""
        if state_id is None:
            abort(404)
        else:
            state = [i for i in all_states if all_states[i].id == state_id]
            if len(state) == 0:
                abort(404)
            if request.method == 'DELETE':
                del all_states[state_id]
                storage.save()
                return make_response(jsonify({}), 200)
            else:
                try:
                    value = request.get_json()
                except Exception:
                    return make_response(jsonify({'error': 'Not a JSON'}), 400)
                else:
                    for i in value:
                        ignore = ['id', 'created_at', 'updated_at']
                        if i not in ignore:
                            setattr(all_states[state_id], i, value.get(i))
                            storage.save()
                    return make_response(jsonify(state[0].to_dict()), 201)