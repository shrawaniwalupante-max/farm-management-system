from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, login_required, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

app.secret_key = "farmproject"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmers.db'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True)

    email = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(200))


class Register(db.Model):

    rid = db.Column(db.Integer, primary_key=True)

    farmername = db.Column(db.String(100))

    adharnumber = db.Column(db.String(50))

    age = db.Column(db.Integer)

    gender = db.Column(db.String(50))

    phonenumber = db.Column(db.String(50))

    address = db.Column(db.String(200))

    farming = db.Column(db.String(100))


class Farming(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    fid = db.Column(db.String(50))

    farmername = db.Column(db.String(100))

    email = db.Column(db.String(100))

    phone = db.Column(db.String(50))

    address = db.Column(db.String(200))

    farmingtype = db.Column(db.String(100))

    crop = db.Column(db.String(100))

    season = db.Column(db.String(100))

    timestamp = db.Column(db.String(100))


class Addagroproducts(db.Model):

    pid = db.Column(db.Integer, primary_key=True)

    productname = db.Column(db.String(100))

    category = db.Column(db.String(100))

    price = db.Column(db.String(50))

    farmername = db.Column(db.String(100))

    email = db.Column(db.String(100))

    image = db.Column(db.String(200))


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


@app.route("/")
def home():

    fruits = Addagroproducts.query.filter_by(category="fruits").all()

    seeds = Addagroproducts.query.filter_by(category="seeds").all()

    others = Addagroproducts.query.filter_by(category="others").all()

    return render_template(
        "index.html",
        fruits=fruits,
        seeds=seeds,
        others=others
    )


@app.route("/register", methods=["GET", "POST"])
@login_required
def register():

    if request.method == "POST":

        farmer = Register(

            farmername=request.form.get("farmername"),

            adharnumber=request.form.get("adharnumber"),

            age=request.form.get("age"),

            gender=request.form.get("gender"),

            phonenumber=request.form.get("phonenumber"),

            address=request.form.get("address"),

            farming=request.form.get("farming")
        )

        db.session.add(farmer)

        db.session.commit()

        flash("Farmer Registered Successfully", "success")

        return redirect("/farmerdetails")

    return render_template("register.html")


@app.route("/addfarming", methods=["GET", "POST"])
@login_required
def addfarming():

    if request.method == "POST":

        fid = request.form.get("fid")

        crop = request.form.get("crop")

        season = request.form.get("season")

        farmer = Register.query.first()

        farming = Farming(

            fid=f"FM{fid}",

            farmername=farmer.farmername if farmer else "Unknown Farmer",

            email="farmer@gmail.com",

            phone=farmer.phonenumber if farmer else "N/A",

            address=farmer.address if farmer else "N/A",

            farmingtype=farmer.farming if farmer else "Organic Farming",

            crop=crop,

            season=season,

            timestamp=datetime.now().strftime("%d-%m-%Y %H:%M")
        )

        db.session.add(farming)

        db.session.commit()

        flash("Farming Record Added Successfully", "success")

        return redirect("/records")

    return render_template("addfarming.html")


@app.route("/farmerdetails")
@login_required
def farmerdetails():

    farmers = Register.query.all()

    return render_template(
        "farmerdetails.html",
        farmers=farmers
    )


@app.route("/records")
@login_required
def records():

    records = Farming.query.all()

    return render_template(
        "records.html",
        records=records
    )


@app.route("/agroproducts")
@login_required
def agroproducts():

    fruits = [

        ("Apples.jpg", "Apple", "₹180/kg"),

        ("Banana.jpg", "Banana", "₹60/dozen"),

        ("Mango.jpg", "Mango", "₹220/kg"),

        ("Watermelon.jpg", "Watermelon", "₹90/kg"),

        ("Strawberry.jpg", "Strawberry", "₹300/kg"),

        ("Orangejpg.jpg", "Orange", "₹120/kg"),

        ("Grapes.jpg", "Grapes", "₹150/kg"),

        ("Guava.jpg", "Guava", "₹80/kg"),

        ("Blueberry.jpg", "Blueberry", "₹450/kg"),

        ("tomato.jpg", "Tomato", "₹70/kg"),

        ("Potato.jpg", "Potato", "₹50/kg"),

        ("Onion.jpg", "Onion", "₹55/kg"),

        ("Carrots.jpg", "Carrot", "₹65/kg"),

        ("Cucumber.jpg", "Cucumber", "₹45/kg"),

        ("Okra.jpg", "Okra", "₹60/kg")
    ]

    seeds = [

        ("wheat.jpg", "Wheat", "₹150/kg"),

        ("Rice.jpg", "Rice", "₹200/kg"),

        ("Jowar.jpg", "Jowar", "₹130/kg"),

        ("Masoor.jpg", "Masoor", "₹160/kg"),

        ("Moong.jpg", "Moong", "₹170/kg"),

        ("Pumpkin Seeds.jpg", "Pumpkin Seeds", "₹250/kg"),

        ("Flax Seeds.jpg", "Flax Seeds", "₹280/kg"),

        ("Pistachio.jpg", "Pistachio", "₹500/kg"),

        ("Cashews.jpg", "Cashews", "₹650/kg"),

        ("Almonds.jpg", "Almonds", "₹700/kg")
    ]

    others = [

        ("cotton.jpg", "Cotton", "₹300/kg"),

        ("Jute.jpg", "Jute", "₹220/kg"),

        ("Rubber.jpg", "Rubber", "₹350/kg"),

        ("Sugarcane.jpg", "Sugarcane", "₹120/kg"),

        ("Rose.jpg", "Rose", "₹250/bundle"),

        ("Tulip.jpg", "Tulip", "₹400/bundle")
    ]

    return render_template(

        "agroproducts.html",

        fruits=fruits,

        seeds=seeds,

        others=others
    )


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form.get("username")

        email = request.form.get("email")

        password = generate_password_hash(
            request.form.get("password")
        )

        user = User(

            username=username,

            email=email,

            password=password
        )

        db.session.add(user)

        db.session.commit()

        flash("Signup Successful", "success")

        return redirect("/login")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")

        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            flash("Login Successful", "success")

            return redirect("/")

        else:

            flash("Invalid Credentials", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged Out Successfully", "success")

    return redirect("/login")


app.app_context().push()

db.create_all()

if __name__ == "__main__":

    app.run(debug=True)