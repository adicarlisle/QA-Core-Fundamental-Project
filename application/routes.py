from application import db, app
from application.models import Users, Dice, History
from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

#Testing the database with dummy data
db.drop_all()
db.create_all()
adi = Users(username="Adi", email="adicarlisle@gmail.com", password="password", first_name="Adi",last_name="Carlisle")
dice1 = Dice(level=2, range=10)
db.session.add(adi)
db.session.commit()
db.session.add(dice1)
db.session.commit()
# entry = History(user = Users.query.filter_by(id=1).first(), dice = Dice.query.filter_by(id=1).first())
# db.session.add(entry)
# db.session.commit()

# class BasicForm(FlaskForm):
#     username = StringField("Username: ")
#     email = StringField("Email: ")
#     password = StringField("Password: ")
#     first_name = StringField("First name: ")
#     last_name = StringField("Last name: ")
#     submit = SubmitField("Send data")

# form = BasicForm()

@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/register", methods=["GET","POST"])
# def register():
#     if request.method == "POST":
#         username = form.username.data
