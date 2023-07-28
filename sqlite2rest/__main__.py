import argparse
from .app import create_app
from .database import Database
from .openapi import get_openapi_spec

def main():
    # Create the top-level parser
    parser = argparse.ArgumentParser(description='SQLite2REST commands.')
    subparsers = parser.add_subparsers(dest='command')

    # Create the parser for the "serve" command
    parser_serve = subparsers.add_parser('serve', help='Start a Flask server for an SQLite database.')
    parser_serve.add_argument('database', help='The path to the SQLite database.')

    # Create the parser for the "spec" command
    parser_spec = subparsers.add_parser('spec', help='Generate OpenAPI spec from SQLite database.')
    parser_spec.add_argument('database', help='The path to the SQLite database.')

    # Parse command-line arguments
    args = parser.parse_args()

    # Execute the appropriate command
    if args.command == 'spec':
        # Create the Flask app
        app = create_app(args.database)
        
        # Create an application context
        with app.app_context():
            # Generate and print the OpenAPI spec
            print(get_openapi_spec(Database(args.database)))
    elif args.command == 'serve':
        # Create and run the Flask app
        app = create_app(args.database)
        app.run()

if __name__ == '__main__':
    main()
