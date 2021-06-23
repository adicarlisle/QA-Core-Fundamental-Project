from application import db, app
from application.models import Users, Dice, History
from flask import render_template

@app.route("/")
def home():
    return render_template("index.html")
