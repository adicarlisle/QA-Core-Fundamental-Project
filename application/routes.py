from application import db, app
from application.models import Users, Dice, History
from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

#Testing the database with dummy data


class BasicForm(FlaskForm):
    username = StringField("Username: ")
    email = StringField("Email: ")
    password = StringField("Password: ")
    first_name = StringField("First name: ")
    last_name = StringField("Last name: ")
    submit = SubmitField("Send data")



# @app.route("/")
# def home():
#     return render_template("index.html")

@app.route("/", methods=["GET","POST"])
def register():
    form = BasicForm()
    if request.method == "POST":
        username = form.username.data
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        entry = Users(username=username, email=email, password=password, first_name=first_name,last_name=last_name)
        db.session.add(entry)
        db.session.commit()
    return render_template("index.html", form = form)
