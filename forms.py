"""Forms for flask notes app."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", 
        validators=[InputRequired(), Length(max=20)])
    password = PasswordField(
        "Password", 
        validators=[InputRequired(), Length(min=8, max=100)]
        ) 
    email = StringField(
        "Email", 
        validators=[InputRequired(), Email(), Length(max=50)]) 
    first_name = StringField(
        "First Name", 
        validators=[InputRequired(), Length(max=30)])
    last_name = StringField(
        "Last Name", 
        validators=[InputRequired(), Length(max=30)])

class LoginForm(FlaskForm):
    username = StringField(
        "Username", 
        validators=[InputRequired(), Length(max=20)])
    password = PasswordField(
        "Password", 
        validators=[InputRequired(), Length(min=8, max=100)])

class CSRFOnlyForm(FlaskForm):
    """CSRF Protection only"""