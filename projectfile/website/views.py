from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, User, db, Order
from flask_login import login_required, current_user
from .forms import EventForm
from werkzeug.security import generate_password_hash
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask import current_app

main_bp = Blueprint('main', __name__, template_folder='templates')


@main_bp.route('/event/<int:event_id>', methods=['GET', 'POST'])

def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    comments = Comment.query.filter_by(event_id=event_id).order_by(Comment.date_posted.desc()).all()

    if request.method == 'POST' and 'ticketQuantity' in request.form:
        # Handle ticket booking
        ticketQuantity = int(request.form.get('ticketQuantity'))
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
    elif request.method == 'POST' and 'comment' in request.form:
        # Handle comment submission
        content = request.form.get('comment')
        new_comment = Comment(
            content=content,
            date_posted=datetime.utcnow(),
            user_id=current_user.id,
            event_id=event_id
        )
        db.session.add(new_comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('main.event_detail', event_id=event_id))

    return render_template('events.html', event=event, comments=comments)


@main_bp.route('/')
@main_bp.route('/category/<category>')
def index(category=None):
    if category:
        # Convert category to lowercase before filtering
        events = Event.query.filter(Event.category.ilike(category.lower())).all()
    else:
        events = Event.query.all()
    return render_template('index.html', events=events, category=category)


@main_bp.route('/event/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        flash('You are not authorized to edit this event.', 'warning')
        return redirect(url_for('main.index'))
    form = EventForm(obj=event)
    if form.validate_on_submit():
        selected_categories = ', '.join(form.music_categories.data)
        event.title = form.title.data
        event.description = form.description.data
        event.date = form.date.data
        event.time = form.start_time.data
        event.venue = form.location.data
        event.price = form.ticket_price.data
        event.category=selected_categories  # Ensure proper category selection
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('main.event_detail', event_id=event_id))
    
    return render_template('create.html', form=form, event_id=event_id)

@main_bp.route('/event/cancel/<int:event_id>', methods=['POST'])
@login_required
def cancel_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        flash('You are not authorized to cancel this event.', 'warning')
        return redirect(url_for('main.event_detail', event_id=event_id))
    
    db.session.delete(event)  # Delete the event from the database
    db.session.commit()
    flash('Event has been cancelled.', 'success')
    return redirect(url_for('main.index'))



@main_bp.route('/events')
def events():
    return render_template('events.html')

def check_upload_file(form):
  #get file data from form  
  fp = form.image.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH, 'static/img', secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/img/' + secure_filename(filename)
  #save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path 

@main_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = EventForm()
    if form.validate_on_submit():
        if form.image.data:
            image_path = check_upload_file(form)
            # Create a new event instance with the returned image path

            selected_categories = ', '.join(form.music_categories.data)
            new_event = Event(
                title=form.title.data,
                description=form.description.data,
                date=form.date.data,
                time=form.start_time.data,
                venue=form.location.data,
                price=form.ticket_price.data,
                category=selected_categories,
                image=image_path,  # Assuming this stores the relative path
                status='Open',  # Default status when creating an event
                user_id=current_user.id
            )
            db.session.add(new_event)
            db.session.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('main.event_detail', event_id=new_event.id))
        else:
            flash('An image file is required.', 'error')
    return render_template('create.html', form=form)

@main_bp.route('/history')
@login_required  # Ensure only logged-in users can access this page
def history():
    user_id = current_user.id  # Get the logged-in user's ID
    # Fetch orders that belong to the user
    orders = Order.query.filter_by(user_id=user_id).all()
    return render_template('history.html', orders=orders)


