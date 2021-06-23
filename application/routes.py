from application import db, app
from application.models import Users, Dice, History
from flask import render_template

db.drop_all()
db.create_all()
db.session.commit()
@app.route("/")
def home():
    return render_template("index.html")
