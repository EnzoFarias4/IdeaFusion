from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

db = SQLAlchemy()

class Idea(db.Model):
    __tablename__ = 'ideas'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    connected_ideas = relationship(
        'Idea',
        secondary='idea_connections',
        primaryjoin='Idea.id==idea_connections.c.idea_id',
        secondaryjoin='Idea.id==idea_connections.c.connected_idea_id',
        backref='connections'
    )

idea_connections = db.Table('idea_connections',
    db.Column('idea_id', db.Integer, db.ForeignKey('ideas.id'), primary_key=True),
    db.Column('connected_idea_id', db.Integer, db.ForeignKey('ideas.id'), primary_key=True)
)