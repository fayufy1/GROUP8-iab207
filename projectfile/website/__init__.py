from flask import Flask
from flask_bootstrap import Bootstrap5
from .database import db  # Updated import

def create_app():
    app = Flask(__name__)
    Bootstrap5(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        from .views import main_bp
        app.register_blueprint(main_bp)

    return app
