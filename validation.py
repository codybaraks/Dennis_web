from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Regexp


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, message="Your name is too short")])
    email = StringField('Email', validators=[DataRequired(), Email(message="Invalid Email")])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, message="short number provided"),
                                             Regexp('^\d{3}\d{3}\d{4}$',
                                                    message="You must provide 10 char Phone Number FORMAT [0794..]")])
