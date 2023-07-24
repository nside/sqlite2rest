import logging
import sys
from flask import Flask, g
from .database import Database
from .routes import setup_routes

def create_app(database_uri):
    # Initialize Flask app
    app = Flask(__name__)

    def get_db():
        if 'db' not in g:
            g.db = Database(database_uri)
        return g.db
    tables = Database(database_uri).get_tables()
    setup_routes(app, tables, get_db)

    # Configure logging
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    app.logger.addHandler(logging.StreamHandler(sys.stderr))
    app.logger.setLevel(logging.DEBUG)

    @app.teardown_appcontext
    def teardown_db(exception):
        db = g.pop('db', None)

        if db is not None:
            db.close()

    return app
