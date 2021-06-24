from application import db, app
from application.models import Users, Dice, History
from flask import render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt
#Testing the database with dummy data

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
    regloc = url_for("register")
    logloc = url_for("login")
    return render_template("index.html", regloc = regloc,logloc = logloc)

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()
    homeloc = url_for("home")
    logloc = url_for("login")
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
    return render_template("register.html", form = form, message = message, homeloc=homeloc, logloc = logloc)

@app.route("/login", methods=["GET","POST"])
def login():
    homeloc = url_for("home")
    regloc = url_for("register")
    bcrypt = Bcrypt(app)
    form = LoginForm()
    message = ""
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            theHashToCheck = Users.query.filter_by(username=username).first().password
        #     auth = bcrypt.check_password_hash(theHashToCheck, form.password.data)
        #     if auth == True:
        #         return redirect(url_for("dashboard", auth=True))
        # else:
        #     message = "Access denied"
    return render_template("login.html", read=theHashToCheck, form=form, message=message,homeloc=homeloc,regloc=regloc)

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    form = DiceForm()
    newdashboard = url_for("reset")
    all_dice = Dice.query.all()
    if request.method == "POST":
        level = form.level.data
        range = form.range.data
        dice = Dice(level=level,range=range)
        db.session.add(dice)
        db.session.commit()
        all_dice = Dice.query.all()
    return render_template("dashboard.html",reset=newdashboard,form = form, all_dice = all_dice)

@app.route("/dashboard-reset")
def reset():
    db.drop_all()
    db.create_all()
    return redirect("/dashboard")