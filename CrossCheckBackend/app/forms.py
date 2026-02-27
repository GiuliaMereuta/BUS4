from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, Length
from datetime import date


class RegisterForm(FlaskForm):
    name = StringField("Full name:", validators=[DataRequired()])
    username = StringField("Username:", validators=[DataRequired(), Length(min=8)])
    password = PasswordField("Password:", validators=[DataRequired(), Length(min=8)])
    role = SelectField("What's your role?", choices=[
        ("patient", "Patient"),
        ("relative", "Relative of a patient"),
        ("gp", "General Practitioner (GP)")],
        validators=[DataRequired()])


class LoginForm(FlaskForm):
    name = StringField("Full name:", validators=[DataRequired()])
    username = StringField("Username:", validators=[DataRequired(), Length(min=8)])
    password = PasswordField("Password:", validators=[DataRequired(), Length(min=8)])


class HealthForm(FlaskForm):
    date = DateField("Date:", format="%d-%m-%Y", default=date.today, validators=[DataRequired()])
    status = StringField("Health status:", validators=[DataRequired(), Length(max=500)])
    ### or SelectField of specific health issues and a StringField with other info