from flask import Flask
from flask_bootstrap import Bootstrap5
from .views import main_bp  # Ensure this import is correct based on your project structure

def create_app():
    app = Flask(__name__)
    Bootstrap5(app)
    app.register_blueprint(main_bp)
    return app
