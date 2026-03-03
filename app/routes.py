from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, url_for, flash, request, session
from app import app
from app import db
from app.forms import RegisterForm, LoginForm, PatientProfile, HealthLog
from app.models import User, PatientProfile, HealthLog, Checkup

#----------------------------------------------------------------------#
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', session=session)

#----------------------------------------------------------------------#

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!")
            return render_template('register.html', form=form)

        hashed_password = generate_password_hash(form.password.data)
        user = User(
            email=form.email.data,
            password=hashed_password,
            role=form.role.data,
        )
        db.session.add(user)
        db.session.commit()

        if user.role == "patient":
            patient_profile = PatientProfile(
                user_id=user.id,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                date_of_birth=form.date_of_birth.data,
            )
            db.session.add(patient_profile)
            db.session.commit()
            return redirect(url_for("patient_profile", patient_id=user.id))

        flash("Registration successful! Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)

#----------------------------------------------------------------------#

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, form.password.data):
            session.permanent = True
            session["user_id"] = user.id
            session["user_role"] = user.role

            if user.role == "patient":
                profile = PatientProfile.query.filter_by(user_id=user.id).first()
                session["user_name"] = f"{profile.first_name} {profile.last_name}"
            else:
                session["user_name"] = user.email
            flash(f"Welcome back, {session['user_name']}!")
            return redirect(url_for("index"))

        else:
            flash("Invalid email and/or password - please try again!")
    return render_template('login.html', form=form)

#----------------------------------------------------------------------#

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out!")
    return redirect(url_for('login'))

#----------------------------------------------------------------------#

@app.route('/patient/<int:patient_id>', methods=['GET', 'POST'])
def patient_profile(patient_id):
    profile = PatientProfile.query.filter_by(user_id=patient_id).first()
    if not profile:
        flash("Patient profile not found.")
        return redirect(url_for("index"))

    form = PatientProfile(obj=profile)

    if form.validate_on_submit():
        # Update profile fields
        profile.hypertension = form.hypertension.data
        profile.diabetes = form.diabetes.data
        profile.heart_disease = form.heart_disease.data
        profile.arthritis = form.arthritis.data
        profile.osteoporosis = form.osteoporosis.data
        profile.copd = form.copd.data
        profile.stroke = form.stroke.data
        profile.dementia = form.dementia.data
        profile.vision_problems = form.vision_problems.data
        profile.hearing_loss = form.hearing_loss.data
        profile.allergies = form.allergies.data
        profile.smoking_status = form.smoking_status.data
        profile.alcohol_consumption = form.alcohol_consumption.data
        profile.physical_activity = form.physical_activity.data

        db.session.commit()
        flash("Profile updated successfully!")
        return redirect(url_for("index"))

    return render_template("patient_profile.html", form=form, profile=profile)

#----------------------------------------------------------------------#

# display health data
def get_health_data():
    pass

# update health data
def update_health_data():
    pass

# delete health data, only on optional fields
def delete_health_data():
    pass

# COPY PASTE CHECKUP ROUTE FROM THOMAS FORK