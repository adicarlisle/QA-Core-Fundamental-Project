from application import db, app
from application.models import Users, Dice, History
from flask import render_template

db.drop_all()
db.create_all()
adi = Users(username="Adi", email="adicarlisle@gmail.com", password="password", first_name="Adi",last_name="Carlisle")
dice1 = Dice(level=2, range=10)
entry = History(user_id=1,dice_id=1)
db.session.add(adi)
db.session.add(dice1)
db.session.add(entry)
db.session.commit()
@app.route("/")
def home():
    return render_template("index.html")
