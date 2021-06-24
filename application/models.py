from application import db, app
from datetime import datetime
from flask_login import LoginManager, UserMixin

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

class Users(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(1048), nullable=False)
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
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    dice_id = db.Column(db.Integer, db.ForeignKey("dice.id"), nullable=False)
    time_rolled = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    