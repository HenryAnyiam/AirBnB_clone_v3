#!/usr/bin/python3
"""module to handle users api"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users",
                 strict_slashes=False,
                 methods=['GET', 'POST'])
@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def list_user(user_id=None):
    """handle users data"""
    users = storage.all(User).values()
    if user_id is not None:
        user = [i for i in users if i.id == user_id]
        if len(user) == 0:
            abort(404)
    if request.method == 'GET':
        if user_id is None:
            user_list = [i.to_dict() for i in users]
            return jsonify(user_list)
        return jsonify(user[0].to_dict())
    elif request.method == 'POST':
        try:
            value = request.get_json()
        except Exception:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        else:
            if 'name' not in value:
                return make_response(jsonify({'error': 'Missing name'}), 400)
            user = User(name=value.get('name'))
            user.save()
            return make_response(jsonify(user.to_dict()), 201)
    elif request.method == 'DELETE':
        storage.delete(user[0])
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        try:
            value = request.get_json()
        except Exception:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        else:
            ignore = ['id', 'created_at', 'updated_at']
            for i in value:
                if i not in ignore:
                    setattr(user[0], i, value.get(i))
            return make_response(jsonify(user[0].to_dict()), 200)
