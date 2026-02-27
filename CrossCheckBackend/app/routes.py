from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, url_for, flash, request, session
from app import app
from app import db
from app.forms import RegisterForm, LoginForm, HealthForm
from app.models import User, HealthRecord



def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        # session
        hashed_password = generate_password_hash(form.password.data)
        user_id = "///" # generate unique user_id
        user = User(
            user_id=user_id,
            username=form.username.data,
            password_hash=hashed_password,
            role=form.role.data,
        )
        db.session.add(user)
        db.session.commit()
    return redirect(url_for("login"))


def authenticate_user():
    form = LoginForm()
    if form.validate_on_submit():
        pass
        if user and check_password_hash(user.password_hash, form.password.data):
            session["user_id"] = user.id
            return redirect(url_for("login"))
        else:
            return render_template("register", form=form)
# to complete

def get_health_data():
    pass


def update_health_data():
    pass

def generate_auth_code():
    pass

def verify_auth_code():
    pass