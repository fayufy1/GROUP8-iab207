from .database import db  # Import the database instance
from datetime import datetime  # Import datetime for timestamping
from flask_login import UserMixin  # Import UserMixin for user session management

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    first_name = db.Column(db.String(100), nullable=False)  # First name of the user
    surname = db.Column(db.String(100), nullable=False)  # Surname of the user
    email = db.Column(db.String(100), unique=True, nullable=False)  # Unique email address
    password = db.Column(db.String(255), nullable=False)  # Hashed password
    contact_number = db.Column(db.String(20))  # Contact number
    street_address = db.Column(db.String(200))  # Street address
    events = db.relationship('Event', backref='user', lazy=True)  # Relationship to Event
    comments = db.relationship('Comment', backref='user', lazy=True)  # Relationship to Comment
    orders = db.relationship('Order', backref='user', lazy=True)  # Relationship to Order

# Event model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    title = db.Column(db.String(100), nullable=False)  # Event title
    description = db.Column(db.Text)  # Event description
    date = db.Column(db.Date, nullable=False)  # Event date
    time = db.Column(db.Time, nullable=False)  # Event time
    image = db.Column(db.String(400))  # Event image URL
    venue = db.Column(db.String(400))  # Event venue
    status = db.Column(db.String(20), nullable=False)  # Event status (e.g., Open, Sold Out)
    category = db.Column(db.String(50), nullable=False)  # Event category
    price = db.Column(db.Integer)  # Ticket price
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    comments = db.relationship('Comment', backref='event', lazy=True)  # Relationship to Comment

# Comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    content = db.Column(db.Text, nullable=False)  # Comment content
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Timestamp
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)  # Foreign key to Event

# Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    quantity = db.Column(db.Integer, nullable=False)  # Quantity ordered
    date_ordered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Timestamp
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)  # Foreign key to Event
    event = db.relationship('Event')  # Relationship to Event
