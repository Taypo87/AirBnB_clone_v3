#!/usr/bin/python3
"""View for cities objects; handles defualt RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, request, abort, Flask, make_response
from models import storage
from models.state import State
from models.state import City


@app_views.route('/cities', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
@app_views.route('/states/<state_id>/cities', methods=[
    'GET', 'DELETE', 'PUT', 'POST'],
                strict_slashes=False)
def get_cities(state_id=None, city_id=None):
    """retrieves all cities, by id"""
    cities = storage.all(City)
    if request.method == 'GET':
        if city_id is None:
            return jsonify([city.to_dict() for city in cities.values()])

        selected = storage.get(City, city_id)
        if selected is None:
            abort(404)
        return jsonify(selected.to_dict())

    elif request.method == 'POST':
            city_data = request.get_json()
            if not city_data:
                return make_response(jsonify({'error': 'Not a JSON'}), 400)
            if 'name' not in city_data:
                return make_response(jsonify({'error': 'Missing name'}), 400)
            city_add = City(**city_data)
            storage.save()
            return make_response(jsonify(city_add.to_dict()), 201)

    elif request.method == 'DELETE':
        citydelete = storage.get(City, city_id)
        if citydelete is None:
            abort(404)
        storage.delete(citydelete)
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'PUT':
        city_update = storage.get(City, city_id)
        if city_update is None:
            abort(404)
        if request.is_json:
            city_data = request.get_json()
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)

        for key, val in city_data.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(city_update, key, val)
        storage.save()
        return make_response(jsonify(city_update.to_dict()), 200)
