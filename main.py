from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin,
    LoginManager,
    login_user,
    logout_user,
    current_user,
    login_required,
)
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "harshithbhaskar"

login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.context_processor
def inject_user():
    return dict(current_user=current_user)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "farmers.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class Farming(db.Model):
    fid = db.Column(db.Integer, primary_key=True)
    farmingtype = db.Column(db.String(100))


class Addagroproducts(db.Model):
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    pid = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(100))
    productdesc = db.Column(db.String(300))
    price = db.Column(db.Integer)


class Trig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.String(100))
    action = db.Column(db.String(100))
    timestamp = db.Column(db.String(100))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(1000))


class Register(db.Model):
    rid = db.Column(db.Integer, primary_key=True)
    farmername = db.Column(db.String(50))
    adharnumber = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    phonenumber = db.Column(db.String(50))
    address = db.Column(db.String(50))
    farming = db.Column(db.String(50))


def seed_database():
    if Test.query.count() == 0:
        db.session.add(Test(name="harshith"))
    if Farming.query.count() == 0:
        db.session.add(Farming(farmingtype="Seed Farming"))
        db.session.add(Farming(farmingtype="coccon"))
        db.session.add(Farming(farmingtype="silk"))
    if Addagroproducts.query.count() == 0:
        db.session.add(
            Addagroproducts(
                username="test",
                email="test@gmail.com",
                productname="GIRIJA CAULIFLOWER",
                productdesc="Tips for Growing Cauliflower. Well drained medium loam and or sandy loam soils are suitable.",
                price=520,
            )
        )
        db.session.add(
            Addagroproducts(
                username="test",
                email="test@gmail.com",
                productname="COTTON",
                productdesc="Cotton is a soft, fluffy staple fiber that grows in a boll, around the seeds of the cotton.",
                price=563,
            )
        )
        db.session.add(
            Addagroproducts(
                username="arkpro",
                email="arkpro@gmail.com",
                productname="silk",
                productdesc="silk is best business developed from coocon for saries preparation and so on",
                price=582,
            )
        )
    if Trig.query.count() == 0:
        db.session.add(
            Trig(fid="2", action="FARMER UPDATED", timestamp="2021-01-19 23:04:44")
        )
        db.session.add(
            Trig(fid="2", action="FARMER DELETED", timestamp="2021-01-19 23:04:58")
        )
        db.session.add(
            Trig(fid="8", action="Farmer Inserted", timestamp="2021-01-19 23:16:52")
        )
        db.session.add(
            Trig(fid="8", action="FARMER UPDATED", timestamp="2021-01-19 23:17:17")
        )
        db.session.add(
            Trig(fid="8", action="FARMER DELETED", timestamp="2021-01-19 23:18:54")
        )
    if User.query.filter_by(email="demo@fms.com").first() is None:
        db.session.add(User(username="Admin", email="demo@fms.com", password="demo123"))
    db.session.commit()


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/farmerdetails")
@login_required
def farmerdetails():
    query = Register.query.all()
    return render_template("farmerdetails.html", query=query)


@app.route("/agroproducts")
@login_required
def agroproducts():
    query = Addagroproducts.query.all()
    return render_template("agroproducts.html", query=query)


@app.route("/addagroproduct", methods=["POST", "GET"])
@login_required
def addagroproduct():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        productname = request.form.get("productname")
        productdesc = request.form.get("productdesc")
        price = request.form.get("price")
        products = Addagroproducts(
            username=username,
            email=email,
            productname=productname,
            productdesc=productdesc,
            price=price,
        )
        db.session.add(products)
        db.session.commit()
        flash("Product Added", "info")
        return redirect("/agroproducts")
    return render_template("addagroproducts.html")


@app.route("/triggers")
@login_required
def triggers():
    query = Trig.query.all()
    return render_template("triggers.html", query=query)


@app.route("/addfarming", methods=["POST", "GET"])
@login_required
def addfarming():
    if request.method == "POST":
        farmingtype = request.form.get("farming")
        query = Farming.query.filter_by(farmingtype=farmingtype).first()
        if query:
            flash("Farming Type Already Exist", "warning")
            return redirect("/addfarming")
        dep = Farming(farmingtype=farmingtype)
        db.session.add(dep)
        db.session.commit()
        flash("Farming Added", "success")
    return render_template("farming.html")


@app.route("/delete/<string:rid>", methods=["POST", "GET"])
@login_required
def delete(rid):
    post = Register.query.filter_by(rid=rid).first()
    db.session.delete(post)
    db.session.commit()
    trig_entry = Trig(fid=str(rid), action="FARMER DELETED", timestamp="now")
    db.session.add(trig_entry)
    db.session.commit()
    flash("Slot Deleted Successful", "warning")
    return redirect("/farmerdetails")


@app.route("/edit/<string:rid>", methods=["POST", "GET"])
@login_required
def edit(rid):
    if request.method == "POST":
        farmername = request.form.get("farmername")
        adharnumber = request.form.get("adharnumber")
        age = request.form.get("age")
        gender = request.form.get("gender")
        phonenumber = request.form.get("phonenumber")
        address = request.form.get("address")
        farmingtype = request.form.get("farmingtype")
        post = Register.query.filter_by(rid=rid).first()
        post.farmername = farmername
        post.adharnumber = adharnumber
        post.age = age
        post.gender = gender
        post.phonenumber = phonenumber
        post.address = address
        post.farming = farmingtype
        db.session.commit()
        trig_entry = Trig(fid=str(rid), action="FARMER UPDATED", timestamp="now")
        db.session.add(trig_entry)
        db.session.commit()
        flash("Slot is Updated", "success")
        return redirect("/farmerdetails")
    posts = Register.query.filter_by(rid=rid).first()
    farming = Farming.query.all()
    return render_template("edit.html", posts=posts, farming=farming)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist", "warning")
            return render_template("signup.html")
        newuser = User(username=username, email=email, password=password)
        db.session.add(newuser)
        db.session.commit()
        flash("Signup Success Please Login", "success")
        return render_template("login.html")
    return render_template("signup.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and (
            user.password == password or check_password_hash(user.password, password)
        ):
            login_user(user)
            flash("Login Success", "primary")
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials", "warning")
            return render_template("login.html")
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    flash("Logout Successful", "warning")
    return redirect(url_for("login"))


@app.route("/register", methods=["POST", "GET"])
@login_required
def register():
    farming = Farming.query.all()
    if request.method == "POST":
        farmername = request.form.get("farmername")
        adharnumber = request.form.get("adharnumber")
        age = request.form.get("age")
        gender = request.form.get("gender")
        phonenumber = request.form.get("phonenumber")
        address = request.form.get("address")
        farmingtype = request.form.get("farmingtype")
        query = Register(
            farmername=farmername,
            adharnumber=adharnumber,
            age=age,
            gender=gender,
            phonenumber=phonenumber,
            address=address,
            farming=farmingtype,
        )
        db.session.add(query)
        db.session.commit()
        trig_entry = Trig(fid=str(query.rid), action="Farmer Inserted", timestamp="now")
        db.session.add(trig_entry)
        db.session.commit()
        flash("Farmer Registered Successfully", "success")
        return redirect("/farmerdetails")
    return render_template("farmer.html", farming=farming)


@app.route("/test")
def test():
    try:
        Test.query.all()
        return "My database is Connected"
    except:
        return "My db is not Connected"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(debug=True, host="0.0.0.0", port=5000)
