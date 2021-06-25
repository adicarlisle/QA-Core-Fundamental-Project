from flask.helpers import make_response
from application import db, app
from application.models import Users, Dice, History
from flask import render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
# Testing the database with dummy data


db.create_all()


class RegisterForm(FlaskForm):
    username = StringField("Username: ", validators=[
        DataRequired()
    ])
    email = StringField("Email: ", validators=[
        Email(),
        DataRequired()
    ])
    password = PasswordField("Password: ", validators=[
        DataRequired(),
        Length(min=8)
    ])
    first_name = StringField("First name: ")
    last_name = StringField("Last name: ")
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[
        DataRequired()
    ])
    password = PasswordField("Password: ", validators=[
        DataRequired()
    ])
    submit = SubmitField("Login")


class DiceForm(FlaskForm):
    level = IntegerField("Level: ", validators=[
        DataRequired()
    ])
    range = IntegerField("Range: ", validators=[
        DataRequired()
    ])
    submit = SubmitField("Add Dice")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    bcrypt = Bcrypt(app)
    message = ""
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = bcrypt.generate_password_hash(form.password.data)
            first_name = form.first_name.data
            last_name = form.last_name.data
            entry = Users(username=username, email=email, password=password,
                          first_name=first_name, last_name=last_name)
            db.session.add(entry)
            db.session.commit()
        else:
            message = "You have entered incorrect details, the password must be 8 characters long"
    return render_template("register.html", form=form, message=message)


@app.route("/login", methods=["GET", "POST"])
def login():

    homeloc = url_for("home")
    regloc = url_for("register")
    bcrypt = Bcrypt(app)
    form = LoginForm()
    if request.method == "GET":
        return render_template("login.html", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for("dashboard"))
                else:
                    return render_template("denied.html")
    return render_template("login.html", form=form)


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    homeloc = url_for("home")
    regloc = url_for("register")
    logloc = url_for("login")
    # delloc = url_for("reset")
    outloc = url_for("logout")
    form = DiceForm()
    welcomeMessage = f"Hello " + str(current_user.username)
    all_dice = Dice.query.all()
    if request.method == "POST":
        level = form.level.data
        range = form.range.data
        dice = Dice(level=level, range=range)
        db.session.add(dice)
        db.session.commit()
    all_dice = Dice.query.all()
    return render_template("dashboard.html",
                           form=form,
                           welcomeMessage=welcomeMessage,
                           all_dice=all_dice
                           )


@app.route("/reset/<id>", methods=["GET", "POST"])
def reset(id):
    id = int(id)
    item = Dice.query.filter_by(id=id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("dashboard"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    return "Profile"
