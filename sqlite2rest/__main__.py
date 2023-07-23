import argparse
from .app import create_app

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Start a Flask server for an SQLite database.')
    parser.add_argument('database', help='The path to the SQLite database.')
    args = parser.parse_args()

    # Create the Flask app
    app = create_app(args.database)

    # Run the Flask app
    app.run()

if __name__ == '__main__':
    main()
