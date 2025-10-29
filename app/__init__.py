# __init__.py

from flask import Flask
from .db import db, migrate
from .routes.book_routes import book_bp
from .models import book # Newly added import
import os 



def create_app(config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    if config:
        # Merge `config`` into the app's configuration 
        # to override teh app's default settings
        app.config.update(config)

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development'

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(book_bp)

    return app