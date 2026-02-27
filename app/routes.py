from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, url_for, flash, request, session
from app import app
from app import db
from app.forms import RegisterForm, LoginForm, HealthForm
from app.models import User, HealthRecord

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('authenticate_user'))
    return render_template('index.html', session=session)

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        # session
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            last_name=form.last_name.data,
            first_name=form.first_name.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data,
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("authenticate_user"))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def authenticate_user():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session["user_id"] = user.user_id
            return redirect(url_for("index"))
        else:
            flash("Invalid email and/or password - please try again!")
            return redirect(url_for("authenticate_user"))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('authenticate_user'))

# to complete

def get_health_data():
    pass


def update_health_data():
    pass

def generate_auth_code():
    pass

def verify_auth_code():
    pass