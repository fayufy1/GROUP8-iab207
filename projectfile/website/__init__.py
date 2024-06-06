from flask import Flask
from flask_bootstrap import Bootstrap5
from .database import db  # Updated import
from flask_login import LoginManager
from . import auth
from .models import User


def create_app():
    app = Flask(__name__)
    Bootstrap5(app)
    app.config['SECRET_KEY'] = 'fayaaz1'  # Change this to a real, secure key!
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Configure upload folder
    UPLOAD_FOLDER = 'static/img'  # Relative path from your main application directory
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Assuming User model has an id attribute
        return User.query.get(int(user_id))

    with app.app_context():
        from .views import main_bp
        app.register_blueprint(main_bp)
        app.register_blueprint(auth.auth_bp)
        db.create_all()

    return app
