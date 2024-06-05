from flask import Blueprint, render_template, request    
from .models import Event

main_bp = Blueprint('main', __name__, template_folder='templates')

# Define your routes here
@main_bp.route('/')
def index():
    return render_template('index.html')

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

@app.route('/')
def index():
    category = request.args.get('category')
    if category:
        events = Event.query.filter_by(category=category).all()
    else:
        events = Event.query.all()
    return render_template('index.html', events=events)
