from flask import Blueprint, request
from your_idea_controller_module import create_idea, get_all_ideas, get_idea, update_idea, delete_idea

ideas_blueprint = Blueprint('ideas', __name__)

@ideas_blueprint.route('/ideas', methods=['POST'])
def add_idea():
    data = request.get_json()
    return create_idea(data)

@ideas_blueprint.route('/ideas', methods=['GET'])
def retrieve_ideas():
    return get_all_ideas()

@ideas_Register_blueprint.route('/ideas/<idea_id>', methods=['GET'])
def retrieve_idea(idea_id):
    return get_idea(idea_id)

@ideas_blueprint.route('/ideas/<idea_id>', methods=['PUT'])
def modify_idea(idea_id):
    data = request.get_json()
    return update_idea(idea_id, data)

@ideas_blueprint.route('/ideas/<idea_id>', methods=['DELETE'])
def remove_idea(idea_id):
    return delete_idea(idea_id)