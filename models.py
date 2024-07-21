from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_CONNECTION_URL = os.getenv("DATABASE_CONNECTION_URL")

db = SQLAlchemy()

class CreativeIdea(db.Model):
    __tablename__ = 'creative_ideas'
    idea_id = db.Column(db.Integer, primary_key=True)
    idea_title = db.Column(db.String(255), nullable=False)
    idea_description = db.Column(db.Text, nullable=False)
    related_ideas = relationship(
        'CreativeIdea',
        secondary='idea_linkage',
        primaryjoin='CreativeIdea.idea_id==idea_linkage.c.initiator_idea_id',
        secondaryjoin='CreativeIdea.idea_id==idea_linkage.c.related_idea_id',
        backref='related_connections'
    )

    def log_creation(self):
        logger.info(f"New creative idea created: {self.idea_title}")

idea_linkage = db.Table('idea_linkage',
    db.Column('initiator_idea_id', db.Integer, db.ForeignKey('creative_ideas.idea_id'), primary_key=True),
    db.Column('related_idea_id', db.Integer, db.ForeignKey('creative_ideas.idea_id'), primary_key=True)
)