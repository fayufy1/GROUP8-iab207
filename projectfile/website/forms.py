from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired

# creates the login information
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired('Enter your email'), Email('Enter a valid email address')])
    password = PasswordField("Password", validators=[InputRequired('Enter your password')])
    submit = SubmitField("Login")
    
 # this is the registration form
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    surname = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
    submit = SubmitField("Sign Up")

