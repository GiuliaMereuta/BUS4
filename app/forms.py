from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, Length
from datetime import date


class RegisterForm(FlaskForm):
    last_name = StringField("Last name:", validators=[DataRequired()])
    first_name = StringField("First name(s):", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Length(min=8)])
    password = PasswordField("Password:", validators=[DataRequired(), Length(min=8)])
    role = SelectField("What's your role?", choices=[
        ("patient", "Patient"),
        ("relative", "Relative of a patient"),
        ("gp", "General Practitioner (GP)")],
        validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Login")


class HealthForm(FlaskForm):
    date = DateField("Date:", format="%d-%m-%Y", default=date.today, validators=[DataRequired()])
    status = StringField("Health status:", validators=[DataRequired(), Length(max=500)])
    ### or SelectField of specific health issues and a StringField with other info