from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# this is a hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        user_email = login_form.email.data  # Assuming your LoginForm has an 'email' field
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.email == user_email))
        if user is None:
            error = 'Incorrect email'
        elif not check_password_hash(user.password, password):  # takes the hash and cleartext password
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            nextp = request.args.get('next')  # this gives the URL from where the login page was accessed
            print(nextp)
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            # Correct method usage here
            hashed_password = generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(
                first_name=form.first_name.data,
                surname=form.surname.data,
                email=form.email.data,
                street_address = form.street_address.data,
                contact_number = form.contact_number.data,
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully signed up!', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Email already exists.', 'error')
    return render_template('signup.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))