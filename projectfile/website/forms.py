from flask_wtf import FlaskForm  # Import FlaskForm base class
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField  # Import form fields
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired  # Import validators
from wtforms import DateField, SelectField, FileField, BooleanField, FormField, TimeField, DecimalField, SelectMultipleField, widgets  # Additional form fields and widgets

# Login form
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired('Enter your email'), Email('Enter a valid email address')])
    password = PasswordField("Password", validators=[InputRequired('Enter your password')])
    submit = SubmitField("Login")
    
# Registration form
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    surname = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    street_address = StringField("Street Address", validators=[DataRequired()])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(min=6, max=15, message="Enter a valid phone number")])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
    submit = SubmitField("Sign Up")

# Custom field for multiple checkboxes
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

# Event form
class EventForm(FlaskForm):
    title = StringField('Event Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    organizer_name = StringField('Organizer Name', validators=[DataRequired()])
    organizer_contact = StringField('Organizer Contact', validators=[DataRequired()])
    ticket_type = SelectMultipleField('Ticket Type', choices=[('general', 'General'), ('vip', 'VIP')], coerce=str)
    ticket_price = StringField('Price ($)', validators=[DataRequired()])
    music_categories = SelectMultipleField('Music Categories', choices=[('pop', 'Pop'), ('rock', 'Rock'), ('electronic', 'Electronic')], coerce=str)
    description = TextAreaField('Event Description', validators=[DataRequired()])
    image = FileField('Event Image', validators=[DataRequired()])
    status = SelectField('Event Status', choices=[('Open', 'Open'), ('Inactive', 'Inactive'), ('Sold Out', 'Sold Out'), ('Cancelled', 'Cancelled')], validators=[DataRequired()])
    submit = SubmitField('Create/Update Event')
