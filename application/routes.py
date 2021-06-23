from application import db, app
from application.models import Users, Dice, History
from flask import render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt
#Testing the database with dummy data


class BasicForm(FlaskForm):
    username = StringField("Username: ", validators=[
        DataRequired()
    ])
    email = StringField("Email: ", validators=[
        DataRequired()
    ])
    password = PasswordField("Password: ", validators=[
        DataRequired(),
        Length(min=8)
    ])
    first_name = StringField("First name: ")
    last_name = StringField("Last name: ")
    submit = SubmitField("Send data")



@app.route("/")
def home():
    regloc = url_for("register")
    logloc = url_for("login")
    return render_template("index.html", regloc = regloc,logloc = logloc)

@app.route("/register", methods=["GET","POST"])
def register():
    form = BasicForm()
    bcrypt = Bcrypt(app)
    message = ""
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = bcrypt.generate_password_hash(form.password.data)
            first_name = form.first_name.data
            last_name = form.last_name.data
            entry = Users(username=username, email=email, password=password, first_name=first_name,last_name=last_name)
            db.session.add(entry)
            db.session.commit()
        else:
            message = "You have entered incorrect details, the password must be 8 characters long"
    return render_template("register.html", form = form, message = message)

@app.route("/login", methods=["GET","POST"])
def login():
    return "Login"