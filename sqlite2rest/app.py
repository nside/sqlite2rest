import logging
import sys
from flask import Flask, g
from .routes import setup_routes

def create_app(database_uri):
    # Initialize Flask app
    app = Flask(__name__)

    setup_routes(app, database_uri)

    # Configure logging
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    app.logger.addHandler(logging.StreamHandler(sys.stderr))
    app.logger.setLevel(logging.DEBUG)

    return app
