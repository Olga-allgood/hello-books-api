# __init__.py

from flask import Flask
from app.routes.book_routes import book_bp

def create_app():
    app = Flask(__name__)

    # Register Blueprints here
    app.register_blueprint(book_bp)

    return app