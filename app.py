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

class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        return f"<Idea {self.title}>"

@app.before_request
def before_request_func():
    if request.is_json:
        try:
            request.json = request.get_json()
        except Exception as e:
            app.logger.error(f"Error parsing JSON: {e}")
            return jsonify({'error': 'Bad request'}), 400
    else:
        request.json = None

@app.route('/ideas', methods=['POST'])
def add_idea():
    if not request.json or 'title' not in request.json:
        return jsonify({'error': 'Missing title'}), 400

    try:
        new_idea = Idea(title=request.json['title'], description=request.json.get('description', ''))
        db.session.add(new_idea)
        db.session.commit()
        return jsonify({'message': 'Idea created successfully'}), 201
    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({'error': 'Failed to create idea'}), 500

@app.route('/ideas', methods=['GET'])
def get_ideas():
    try:
        ideas_list = Idea.query.all()
        ideas = [{'id': idea.id, 'title': idea.title, 'description': idea.description} for idea in ideas_list]
        return jsonify({'ideas': ideas})
    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({'error': 'Failed to fetch ideas'}), 500

@app.route('/ideas/<int:id>', methods=['GET'])
def get_idea(id):
    try:
        idea = Idea.query.get_or_404(id)
        return jsonify({'id': idea.id, 'title': idea.title, 'description': idea.description})
    except SQLAlchemyError as e:
        app.logger.error(f"Database error when fetching idea {id}: {e}")
        return jsonify({'error': 'Failed to fetch the idea'}), 500

@app.route('/ideas/<int:id>', methods=['PUT'])
def update_idea(id):
    if not request.json:
        return jsonify({'error': 'Not a JSON request'}), 400

    try:
        idea = Idea.query.get_or_404(id)
        idea.title = request.json.get('title', idea.title)
        idea.description = request.json.get('description', idea.description)
        db.session.commit()
        return jsonify({'message': 'Idea updated successfully'})
    except SQLAlchemyError as e:
        app.logger.error(f"Database error while updating idea {id}: {e}")
        return jsonify({'error': 'Failed to update the idea'}), 500

@app.route('/ideas/<int:id>', methods=['DELETE'])
def delete_idea(id):
    try:
        idea = Idea.query.get_or_404(id)
        db.session.delete(idea)
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