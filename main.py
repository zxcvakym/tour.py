import os
import binascii

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash

from data import data
# from data.tours_to_db import data_to_db
from data.base import Session, create_db
from data.models import Tour, User
from data.forms import SignUpForm, LoginForm


app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(24))

login_manager = LoginManager()
login_manager.login_message = "Щоб забронювати тур увійдіть до системи"
login_manager.login_view = "login"
login_manager.init_app(app)


@app.context_processor
def global_data():
    with Session() as session:
        if current_user.is_authenticated:
            user = session.query(User).where(User.id == current_user.id).first()
            user_tours = user.tours
        else:
            user_tours = []

        return dict(departures=data.departures, user_tours=user_tours)


@login_manager.user_loader
def user_loader(user_id):
    with Session() as session:
        return session.query(User).where(User.id == user_id).first()


@app.route('/')
def index():
    with Session() as session:
        tours = session.query(Tour).all()
        return render_template("index.html", tours=tours)


@app.route('/tour/<int:index>/')
def tour(index):
    with Session() as session:
        tour = session.query(Tour).where(Tour.id == index).first()
        return render_template("tour.html", tour=tour)


@app.route('/departure/<dep>/')
def departure(dep):
    with Session() as session:
        tours = session.query(Tour).where(Tour.departure == dep).all()
        return render_template("departure.html", tours=tours, dep=dep)


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    signup_form = SignUpForm()

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        email = signup_form.email.data

        with Session() as session:
            user = session.query(User).where(User.username == username).first()
            if user:
                flash("Користувач з таким логіном вже існує")
                return redirect(url_for("login"))

            password = generate_password_hash(signup_form.password.data)
            user = User(username=username, email=email, password=password)
            session.add(user)
            session.commit()
            flash("Вітаю, Ви успішно зареєструвались")
            return redirect(url_for("login"))

    return render_template("signup.html", form=signup_form)


@app.route("/login/", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        username = login_form.username.data

        with Session() as session:
            user = session.query(User).where(or_(User.username == username, User.email == username)).first()

            if not user or not check_password_hash(user.password, login_form.password.data):
                flash("Логін або пароль невірний")
                return redirect(url_for("login"))

            login_user(user)
            return redirect(url_for("cabinet"))

    return render_template("login.html", form=login_form)


@app.get("/logout/")
@login_required
def logout():
    flash("До побачення.")
    logout_user()
    return redirect(url_for("index"))


@app.get("/reserve/<int:tour_id>/")
@login_required
def reserve(tour_id: int):
    with Session() as session:
        tour = session.query(Tour).where(Tour.id == tour_id).first()
        user = session.query(User).where(User.id == current_user.id).first()
        user.tours.append(tour)
        session.commit()
        flash("Тур успішно заброньовано")
        return redirect(url_for("cabinet"))


@app.get("/cabinet/")
@login_required
def cabinet():
    return render_template("cabinet.html")


if __name__ == "__main__":
    create_db()
    # data_to_db()
    app.run(debug=True)