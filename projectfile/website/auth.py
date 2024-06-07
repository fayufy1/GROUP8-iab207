from flask import Blueprint, flash, render_template, request, url_for, redirect  # Import necessary Flask modules
from flask_bcrypt import generate_password_hash, check_password_hash  # Password hashing
from flask_login import login_user, login_required, logout_user  # User session management
from .models import User  # User model
from .forms import LoginForm, RegisterForm  # Login and registration forms
from . import db  # Database instance

# Authentication blueprint
auth_bp = Blueprint('auth', __name__)

# Login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        user_email = login_form.email.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.email == user_email))
        if user is None:
            error = 'Incorrect email'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            nextp = request.args.get('next')
            if not nextp or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        flash(error)
    return render_template('user.html', form=login_form, heading='Login')

# Signup route
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if not existing_user:
            hashed_password = generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(
                first_name=form.first_name.data,
                surname=form.surname.data,
                email=form.email.data,
                street_address=form.street_address.data,
                contact_number=form.contact_number.data,
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully signed up!', 'success')
            return redirect(url_for('auth.login'))
        flash('Email already exists.', 'error')
    return render_template('signup.html', form=form)

# Logout route
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
