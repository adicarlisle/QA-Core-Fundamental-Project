from flask.helpers import make_response
from application import db, app
from application.models import Users, Dice, History
from flask import render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from random import randint
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
    submit = SubmitField("Submit")


class HistoryForm(FlaskForm):
    submit = SubmitField("Roll")


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
    form = DiceForm()
    if current_user.is_anonymous:
        welcomeMessage = "Hello Anonymous"
    else: 
        welcomeMessage = f"Hello " + str(current_user.username)
    if request.method == "POST":
        level = form.level.data
        range = form.range.data
        dice = Dice(level=level, range=range)
        db.session.add(dice)
        db.session.commit()
    all_dice = Dice.query.all()
    history = History.query.all()
    return render_template("dashboard.html",
                           form=form,
                           welcomeMessage=welcomeMessage,
                           all_dice=all_dice,
                           history=history
                           )


@app.route("/reset-dice/<id>", methods=["GET", "POST"])
def reset_dice(id):
    id = int(id)
    for i in range(len(History.query.all())):
        item = History.query.first()
        i += 1
        db.session.delete(item)

    db.session.commit()
    item = Dice.query.filter_by(id=id).first()
    db.session.delete(item)
    db.session.commit()

    return redirect(url_for("dashboard"))

@app.route("/reset-history/", methods=["GET", "POST"])
def reset_history():
    for i in range(len(History.query.all())):
        item = History.query.first()
        i += 1
        db.session.delete(item)

    db.session.commit()
    return redirect(url_for("dashboard"))


@app.route("/update/<id>", methods=["GET", "POST"])
def update(id):
    form = DiceForm()
    id = int(id)
    item = Dice.query.filter_by(id=id).first()
    if request.method == "POST":
        if form.validate_on_submit():
            item.level = form.level.data
            item.range = form.range.data
            db.session.commit()
            return redirect(url_for("dashboard"))
    return render_template("update.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/roll/<dice>", methods=["GET","POST"])
@login_required
def roll(dice):
    user_item = Users.query.filter_by(username=current_user.username).first().id
    dice = int(dice)
    dice_item = Dice.query.filter_by(id=dice).first()
    entry = History(user_id=user_item,
                    dice_id=dice_item.id,
                    value=dice_item.level*randint(0,dice_item.range)
                    )
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for("dashboard"))
 