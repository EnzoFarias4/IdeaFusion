from flask import Blueprint, request, jsonify, Response
from your_idea_controller_module import (create_new_idea, fetch_all_ideas, 
                                         fetch_single_idea, update_existing_idea, 
                                         remove_existing_idea, rate_idea, 
                                         fetch_idea_rating)

ideas_api_blueprint = Blueprint('ideas_api', __name__)

@ideas_api_blueprint.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

def validate_idea_data(idea_data):
    return idea_data is not None and 'title' in idea_data

@ideas_api_blueprint.route('/ideas', methods=['POST'])
def add_new_idea():
    idea_data = request.get_json()
    if not validate_idea_data(idea_data):
        return Response("Invalid idea data", status=400)
    response = create_new_idea(idea_data)
    if not response:
        return Response("Failed to create new idea", status=500)
    return response, 201

@ideas_api_blueprint.route('/ideas', methods=['GET'])
def get_ideas():
    try:
        return fetch_all_ideas()
    except Exception as e:
        return jsonify(error=str(e)), 500

@ideas_api_blueprint.route('/ideas/<idea_id>', methods=['GET'])
def get_specific_idea(idea_id):
    try:
        return fetch_single_idea(idea_id)
    except Exception as e:
        return jsonify(error=str(e)), 404

@ideas_api_blueprint.route('/ideas/<idea_id>', methods=['PUT'])
def update_idea(idea_id):
    updated_idea_data = request.get_json()
    try:
        return update_existing_idea(idea_id, updated_idea_data)
    except Exception as e:
        return jsonify(error=str(e)), 500

@ideas_api_blueprint.route('/ideas/<idea_id>', methods=['DELETE'])
def delete_idea(idea_id):
    try:
        return remove_existing_idea(idea_id)
    except Exception as e:
        return jsonify(error=str(e)), 500

@ideas_api_blueprint.route('/ideas/<idea_id>/rate', methods=['POST'])
def rate_an_idea(idea_id):
    rating_data = request.get_json()
    try:
        return rate_idea(idea_id, rating_data)
    except Exception as e:
        return jsonify(error=str(e)), 500

@ideas_api_blueprint.route('/ideas/<idea_id>/rating', methods=['GET'])
def get_idea_rating(idea_id):
    try:
        return fetch_idea_rating(idea_id)
    except Exception as e:
        return jsonify(error=str(e)), 404