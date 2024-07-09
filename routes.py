from flask import Blueprint, request
from your_idea_controller_module import create_new_idea, fetch_all_ideas, fetch_single_idea, update_existing_idea, remove_existing_idea

ideas_api_blueprint = Blueprint('ideas_api', __name__)

@ideas_api_blueprint.route('/ideas', methods=['POST'])
def add_new_idea():
    idea_data = request.get_json()
    return create_new_idea(idea_data)

@ideas_api_blueprint.route('/ideas', methods=['GET'])
def get_ideas():
    return fetch_all_ideas()

@ideas_api_blueprint.route('/ideas/<idea_id>', methods=['GET'])
def get_specific_idea(idea_id):
    return fetch_single_idea(idea_id)

@ideas_api_blueprint.route('/ideas/<idea_id>', methods=['PUT'])
def update_idea(idea_id):
    updated_idea_data = request.get_json()
    return update_existing_idea(idea_id, updated_idea_data)

@ideas_api_blueprint.route('/ideas/<idea_id>', methods=['DELETE'])
def delete_idea(idea_id):
    return remove_existing_idea(idea_id)