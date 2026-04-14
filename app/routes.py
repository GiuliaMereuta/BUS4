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

    if request.method == "POST":
        print("POST request received")

    if form.validate_on_submit():
        print("Form validation passed")

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

        print("User saved:", user.email)

        flash("Registration successful!")
        return redirect(url_for("login"))

    else:
        if request.method == "POST":
            print("Form errors:", form.errors)

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

                if profile:
                    session["user_name"] = f"{profile.first_name} {profile.last_name}"
                else:
                    session["user_name"] = user.email
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
@app.route('/health', methods=['GET'])
def get_health_data():
    if "user_id" not in session:
        flash("Please log in first.")
        return redirect(url_for("login"))

    # Get patient profile
    profile = PatientProfile.query.filter_by(user_id=session["user_id"]).first()

    if not profile:
        flash("Patient profile not found.")
        return redirect(url_for("index"))

    # Get all health logs (latest first)
    logs = HealthLog.query.filter_by(patient_id=profile.id)\
                          .order_by(HealthLog.created_at.desc())\
                          .all()

    return render_template("health_logs.html", logs=logs)

#----------------------------------------------------------------------#
# update health data
@app.route('/health/update/<int:log_id>', methods=['GET', 'POST'])
def update_health_data(log_id=None):
    if "user_id" not in session:
        flash("Please log in first.")
        return redirect(url_for("login"))

    form = HealthLog()

    profile = PatientProfile.query.filter_by(user_id=session["user_id"]).first()

    if not profile:
        flash("Patient profile not found.")
        return redirect(url_for("index"))

    log = None

    # If editing existing log
    if log_id:
        log = HealthLog.query.filter_by(id=log_id, patient_id=profile.id).first()
        if not log:
            flash("Health log not found.")
            return redirect(url_for("get_health_data"))

        if request.method == "GET":
            form = HealthLog(obj=log)

    if form.validate_on_submit():
        # CREATE
        if not log:
            log = HealthLog(
                patient_id=profile.id,
                temperature=form.temperature.data,
                bp_systolic=form.bp_systolic.data,
                bp_diastolic=form.bp_diastolic.data,
                mood=form.mood.data,
                notes=form.notes.data
            )
            db.session.add(log)

        # UPDATE
        else:
            log.temperature = form.temperature.data
            log.bp_systolic = form.bp_systolic.data
            log.bp_diastolic = form.bp_diastolic.data
            log.mood = form.mood.data
            log.notes = form.notes.data

        db.session.commit()
        flash("Health data saved successfully!")
        return redirect(url_for("get_health_data"))

    return render_template("health_form.html", form=form, log=log)
#----------------------------------------------------------------------#
# delete health data, only on optional fields
@app.route('/health/delete/<int:log_id>', methods=['POST'])
def delete_health_data(log_id):
    if "user_id" not in session:
        flash("Please log in first.")
        return redirect(url_for("login"))

    profile = PatientProfile.query.filter_by(user_id=session["user_id"]).first()

    if not profile:
        flash("Patient profile not found.")
        return redirect(url_for("index"))

    log = HealthLog.query.filter_by(id=log_id, patient_id=profile.id).first()

    if not log:
        flash("Health log not found.")
        return redirect(url_for("get_health_data"))

    db.session.delete(log)
    db.session.commit()

    flash("Health log deleted.")
    return redirect(url_for("get_health_data"))
#----------------------------------------------------------------------#

# COPY PASTE CHECKUP ROUTE FROM THOMAS FORK