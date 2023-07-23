from flask import current_app
from openapi_spec_validator import validate_spec
import yaml

def generate_openapi_spec():
    # Basic OpenAPI spec
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "SQLite2REST",
            "version": "1.0.0"
        },
        "paths": {}
    }

    # Generate paths for each route
    for rule in current_app.url_map.iter_rules():
        # Skip the static routes
        if rule.endpoint in ('static', 'openapi'):
            continue

        # Initialize the path item object
        if str(rule) not in spec["paths"]:
            spec["paths"][str(rule)] = {}

        path_item = spec["paths"][str(rule)]

        # Add an operation object for each method
        for method in rule.methods:
            if method in ['GET', 'POST', 'PUT', 'DELETE']:
                operation = {
                    'GET': 'Retrieve all records from',
                    'POST': 'Create a new record in',
                    'PUT': 'Update a record in',
                    'DELETE': 'Delete a record from',
                    'PATCH': 'Partially update a record in',
                    'TRACE': 'Trace a request to'
                }.get(method, 'Perform operation on')

                table_name = str(rule).split('/')[1]

                path_item[method.lower()] = {
                    "summary": f"{operation} the {table_name} table",
                    "responses": {
                        "200": {
                            "description": "OK"
                        }
                    }
                }

    # Validate the spec
    validate_spec(spec)

    # Return the spec as a dictionary
    return spec

def get_openapi_spec():
    spec = generate_openapi_spec()
    return yaml.dump(spec)

