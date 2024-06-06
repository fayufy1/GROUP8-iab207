from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, User, db, Order
from flask_login import login_required, current_user
from .forms import RegisterForm
from werkzeug.security import generate_password_hash
from datetime import datetime

main_bp = Blueprint('main', __name__, template_folder='templates')



@main_bp.route('/event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    comments = Comment.query.filter_by(event_id=event_id).order_by(Comment.date_posted.desc()).all()

    if request.method == 'POST':
        # Handling the form submission for booking tickets
        fullName = request.form.get('fullName')  # Assuming you might use it later
        email = request.form.get('email')  # Assuming you might use it later
        ticketQuantity = int(request.form.get('ticketQuantity'))  # Ensure 'ticketQuantity' is correct in your form

        new_order = Order(
            quantity=ticketQuantity,
            date_ordered=datetime.utcnow(),
            user_id=current_user.id,
            event_id=event_id
        )
        db.session.add(new_order)
        db.session.commit()
        flash('Your tickets have been booked successfully!', 'success')
        return redirect(url_for('main.history'))

    # The same view is used for GET requests to display the page
    return render_template('events.html', event=event, comments=comments)

@main_bp.route('/')
@main_bp.route('/category/<category>')
def index(category=None):
    if category:
        events = Event.query.filter_by(category=category).all()
    else:
        events = Event.query.all()
    return render_template('index.html', events=events, category=category)


@main_bp.route('/events')
def events():
    return render_template('events.html')

@main_bp.route('/create')
def create():
    return render_template('create.html')

@main_bp.route('/history')
@login_required  # Ensure only logged-in users can access this page
def history():
    user_id = current_user.id  # Get the logged-in user's ID
    # Fetch orders that belong to the user
    orders = Order.query.filter_by(user_id=user_id).all()
    return render_template('history.html', orders=orders)


