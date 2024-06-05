from flask import Blueprint, render_template, request, redirect, url_for, abort
from .models import Event, Comment  # Assuming db is not used directly here
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
@main_bp.route('/category/<category>')
def index(category=None):
    if category:
        # This filters events by category
        events = Event.query.filter_by(category=category).all()
    else:
        # This fetches all events if no category is specified
        events = Event.query.all()
    return render_template('index.html', events=events, category=category)

@main_bp.route('/event/<int:event_id>')
def event_detail(event_id):
    # Fetch the event or return 404 if not found
    event = Event.query.get_or_404(event_id)
    # Fetch comments related to the event
    comments = Comment.query.filter_by(event_id=event_id).order_by(Comment.date_posted.desc()).all()
    return render_template('events.html', event=event, comments=comments)

@main_bp.route('/events')
def events():
    return render_template('events.html')

@main_bp.route('/create')
def create():
    return render_template('create.html')

@main_bp.route('/history')
def history():
    return render_template('history.html')

@main_bp.route('/signup')
def signup():
    return render_template('signup.html')

@main_bp.route('/login')
def login():
    return render_template('login.html')
