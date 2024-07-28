from app import db
from sqlalchemy.sql import func

class GameRound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_choice = db.Column(db.String(10), nullable=False)
    ai_choice = db.Column(db.String(10), nullable=False)
    winner = db.Column(db.String(10), nullable=False)
    model_used = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())