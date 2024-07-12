from flask import Blueprint, request
from your_idea_controller_module import create_new_idea, fetch_all_ideas, fetch_single_idea, update_existing_idea, remove_existing_idea, rate_idea, fetch_idea_rating

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

@ideas_api_blueprint.route('/ideas/<idea_id>/rate', methods=['POST'])
def rate_an_idea(idea_id):
    rating_data = request.get_json()
    return rate_idea(idea_id, rating_data)

@ideas_api_blueprint.route('/ideas/<idea_id>/rating', methods=['GET'])
def get_idea_rating(idea_id):
    return fetch_idea_rating(idea_id)
```

```python
def rate_idea(idea_id, rating_data):
    """
    Update the provided idea with a new rating.
    :param idea_id: The ID of the idea to be rated.
    :param ratingody): JSON containing the rating details.
    :return: A response indicating the success or failure of the operation.
    """
    pass

def fetch_idea_rating(idea_id):
    """
    Retrieve the average rating of a specific idea.
    :param idea_id: The ID of the idea.
    :return: The average rating of the idea.
    """
    pass