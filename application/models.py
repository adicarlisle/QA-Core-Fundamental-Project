from sqlalchemy.orm import backref
from application import db
from datetime import datetime

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    history = db.relationship("History", backref="user")

class Dice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer)
    range = db.Column(db.Integer)
    history = db.relationship("History", backref="dice")

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    dice_id = db.Column(db.Integer, db.ForeignKey("dice.id"), nullable=False)
    time_rolled = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #TODO value, calculate from level and range in the format Level: 2 Range: 10 -> (0-10) (0-10) 