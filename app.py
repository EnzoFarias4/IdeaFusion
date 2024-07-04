from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class IdeaModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        return f"<IdeaModel {self.title}>"

@app.before_request
def check_for_json_request():
    if request.is_json:
        try:
            request.json_data = request.get_json()
        except Exception as e:
            app.logger.error(f"Error parsing JSON: {e}")
            return jsonify({'error': 'Bad request'}), 400
    else:
        request.json_data = None

@app.route('/ideas', methods=['POST'])
def create_idea():
    json_data = request.get_json(silent=True)
    if not json_data or 'title' not in json_data:
        return jsonify({'error': 'Missing title'}), 400

    try:
        new_idea = IdeaModel(title=json_data['title'], description=json_data.get('description', ''))
        db.session.add(new_idea)
        db.session.commit()
        return jsonify({'message': 'Idea created successfully'}), 201
    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({'error': 'Failed to create idea'}), 500

@app.route('/ideas', methods=['GET'])
def fetch_all_ideas():
    try:
        ideas_query = IdeaModel.query.all()
        ideas_list = [{'id': idea.id, 'title': idea.title, 'description': idea.description} for idea in ideas_query]
        return jsonify({'ideas': ideas_list})
    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({'error': 'Failed to fetch ideas'}), 500

@app.route('/ideas/<int:id>', methods=['GET'])
def fetch_single_idea(id):
    try:
        idea = IdeaModel.query.get_or_404(id)
        return jsonify({'id': idea.id, 'title': idea.title, 'description': idea.description})
    except SQLAlchemyError as e:
        app.logger.error(f"Database error when fetching idea {id}: {e}")
        return jsonify({'error': 'Failed to fetch the idea'}), 500

@app.route('/ideas/<int:id>', methods=['PUT'])
def update_single_idea(id):
    json_data = request.get_json(silent=True)
    if not json_data:
        return jsonify({'error': 'Not a JSON request'}), 400

    try:
        idea_to_update = IdeaModel.query.get_or_404(id)
        idea_to_update.title = json_data.get('title', idea_to_update.title)
        idea_to_update.description = json_data.get('description', idea_to_update.description)
        db.session.commit()
        return jsonify({'message': 'Idea updated successfully'})
    except SQLAlchemyError as e:
        app.logger.error(f"Database error while updating idea {id}: {e}")
        return jsonify({'error': 'Failed to update the idea'}), 500

@app.route('/ideas/<int:id>', methods=['DELETE'])
def delete_single_idea(id):
    try:
        idea_to_delete = IdeaModel.query.get_or_404(id)
        db.session.delete(idea_to_delete)
        db.session.commit()
        return jsonify({'message': 'Idea deleted successfully'})
    except SQLAlchemyError as e:
        app.logger.error(f"Database error while deleting idea {id}: {e}")
        return jsonify({'error': 'Failed to delete the idea'}), 500

if __name__ == '__main__':
    try:
        db.create_all()
        app.run(port=5000)
    except Exception as e:
        app.logger.error(f"Failed to start application: {e}")