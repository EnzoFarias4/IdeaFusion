from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from dotenv import load_dotenv
import os

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
        request.json = request.get_json()
    else:
        request.json = None

@app.route('/ideas', methods=['POST'])
def add_idea():
    if not request.json or not 'title' in request.json:
        return jsonify({'error': 'Missing title'}), 400

    new_idea = Idea(title=request.json['title'], description=request.json.get('description', ''))
    db.session.add(new_idea)
    db.session.commit()

    return jsonify({'message': 'Idea created successfully'}), 201

@app.route('/ideas', methods=['GET'])
def get_ideas():
    ideas_list = Idea.query.all()
    ideas = [{'id': idea.id, 'title': idea.title, 'description': idea.description} for idea in ideas_list]

    return jsonify({'ideas': ideas})

@app.route('/ideas/<int:id>', methods=['GET'])
def get_idea(id):
    idea = Idea.query.get_or_404(id)
    return jsonify({'id': idea.id, 'title': ideatoHaveBeenCallediance, 'description': idea.description})

@app.route('/ideas/<int:id>', methods=['PUT'])
def update_idea(id):
    idea = Idea.query.get_or_404(id)

    if not request.json:
        return jsonify({'error': 'Not a JSON request'}), 400

    idea.title = request.json.get('title', idea.title)
    idea.description = request.json.get('description', idea.description)

    db.session.commit()

    return jsonify({'message': 'Idea updated successfully'})

@app.route('/ideas/<int:id>', methods=['DELETE'])
def delete_idea(id):
    idea = Idea.query.get_or_404(id)
    db.session.delete(idea)
    db.session.commit()

    return jsonify({'message': 'Idea deleted successfully'})

if __name__ == '__main__':
    db.createall()
    app.run(port=5000)