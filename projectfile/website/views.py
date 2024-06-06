from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, User, db
from flask_login import login_required, current_user
from .forms import RegisterForm
from werkzeug.security import generate_password_hash
main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
@main_bp.route('/category/<category>')
def index(category=None):
    if category:
        events = Event.query.filter_by(category=category).all()
    else:
        events = Event.query.all()
    return render_template('index.html', events=events, category=category)

@main_bp.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
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


