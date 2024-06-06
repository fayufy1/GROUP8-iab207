from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired
from wtforms import StringField, SubmitField, DateField, SelectField, TextAreaField, FileField,BooleanField, FormField, TimeField, DecimalField, SelectMultipleField, widgets

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


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()



class EventForm(FlaskForm):
    title = StringField('Event Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    organizer_name = StringField('Organizer Name', validators=[DataRequired()])
    organizer_contact = StringField('Organizer Contact', validators=[DataRequired()])
    ticket_type = SelectMultipleField('Ticket Type', choices=[('general', 'General'), ('vip', 'VIP')],coerce=str)
    ticket_price = StringField('Price ($)', validators=[DataRequired()])
    music_categories = SelectMultipleField('Music Categories', choices=[
        ('pop', 'Pop'), ('rock', 'Rock'), ('electronic', 'Electronic'), ('jazz', 'Jazz')
    ], coerce=str)
    description = TextAreaField('Event Description', validators=[DataRequired()])
    image = FileField('Event Image', validators=[DataRequired()])
    status = SelectField('Event Status', choices=[('Open', 'Open'), ('Inactive', 'Inactive'), ('Sold Out', 'Sold Out'), ('Cancelled', 'Cancelled')], validators=[DataRequired()])
    submit = SubmitField('Create/Update Event')