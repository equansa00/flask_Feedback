from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, validators

class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(max=20), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    email = StringField('Email', [validators.Length(max=50), validators.Email(), validators.DataRequired()])
    first_name = StringField('First Name', [validators.Length(max=30), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(max=30), validators.DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class FeedbackForm(FlaskForm):
    title = StringField('Title', validators=[validators.DataRequired()])
    content = TextAreaField('Content', validators=[validators.DataRequired()])
