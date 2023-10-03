#!/usr/bin/python3
"""module to handle places review api"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def list_reviews(place_id=None):
    """list places according to city id"""
    if place_id is None:
        abort(404)
    places = storage.all(Place).values()
    place = [i for i in places if i.id == place_id]
    if len(place) == 0:
        abort(404)
    reviews = storage.all(reviews).values()
    if request.method == 'GET':
        list_review = [i.to_dict() for i in reviews if i.place_id == place_id]
        return jsonify(list_review)
    elif request.method == 'POST':
        try:
            values = request.get_json()
        except Exception:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        else:
            if 'user_id' not in values:
                val = jsonify({'error': 'Missing user_id'})
                return make_response(val, 400)
            users = storage.all(User).values()
            user = [i for i in users if i.id == values['user_id']]
            if len(user) == 0:
                abort(404)
            if 'text' not in values:
                return make_response(jsonify({'error': 'Missing text'}), 400)
            values['place_id'] = place_id
            review = Review(**values)
            review.save()
            return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def find_review(review_id=None):
    """find review with id"""
    if review_id is None:
        abort(404)
    reviews = storage.all(Review).values()
    review = [i for i in reviews if i.id == review_id]
    if len(review) == 0:
        abort(404)
    if request.method == 'GET':
        return jsonify(review[0].to_dict())
    elif request.method == 'PUT':
        ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        try:
            values = request.get_json()
        except Exception:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        else:
            for i in values:
                if i not in ignore:
                    setattr(review[0], i, values.get(i))
                    storage.save()
            return make_response(jsonify(review[0].to_dict()), 200)
    elif request.method == 'DELETE':
        storage.delete(review[0])
        storage.save()
        return make_response(jsonify({}), 200)
