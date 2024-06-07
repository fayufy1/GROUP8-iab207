from flask import Flask, render_template  # Flask for app, render_template for templates
from flask_bootstrap import Bootstrap5  # Bootstrap integration
from .database import db  # Database instance
from flask_login import LoginManager  # User session management
from . import auth  # Authentication blueprint
from .models import User  # User model for user loading

def create_app():
    app = Flask(__name__)  # Create Flask app
    Bootstrap5(app)  # Initialize Bootstrap
    app.config['SECRET_KEY'] = 'fayaaz1'  # Set secret key (change for production)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'  # Database URI
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional SQLAlchemy config
    db.init_app(app)  # Initialize database

    app.config['UPLOAD_FOLDER'] = 'static/img'  # Configure upload folder

    login_manager = LoginManager()  # Login manager setup
    login_manager.login_view = 'auth.login'  # Default login view
    login_manager.init_app(app)  # Initialize login manager

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Load user by ID

    with app.app_context():
        from .views import main_bp  # Import main blueprint
        app.register_blueprint(main_bp)  # Register main blueprint
        app.register_blueprint(auth.auth_bp)  # Register auth blueprint
        db.create_all()  # Create database tables

    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", error=e)  # Custom 404 error handler

    return app  # Return app instance
