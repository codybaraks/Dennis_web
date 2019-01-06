from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Regexp


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=8, message="Your name is too short")])
    email = StringField('Email', validators=[DataRequired(), Email(message="Invalid Email")])
    password = PasswordField('Password', validators=[DataRequired(message="You must provide a password"), Length(min=6, message="Password Too short")])
    country = StringField('country', validators=[DataRequired()])
