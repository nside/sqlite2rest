from flask import current_app
from openapi_spec_validator import validate_spec
import yaml
from . import __version__

def get_operation_summary(method):
    return {
        'GET': 'Retrieve all records from',
        'POST': 'Create a new record in',
        'PUT': 'Update a record in',
        'DELETE': 'Delete a record from',
        'PATCH': 'Partially update a record in',
        'TRACE': 'Trace a request to'
    }.get(method, 'Perform operation on')

def add_paging_parameters(operation_obj):
    operation_obj["parameters"] = [
        {
            "name": "page",
            "in": "query",
            "description": "Page number to retrieve",
            "required": False,
            "schema": {
                "type": "integer",
                "default": 1
            }
        },
        {
            "name": "per_page",
            "in": "query",
            "description": "Number of records per page",
            "required": False,
            "schema": {
                "type": "integer",
                "default": 10
            }
        }
    ]

def add_operation_to_path(path_item, method, rule_str, primary_key_type):
    operation = get_operation_summary(method)
    table_name = rule_str.split('/')[1]
    operation_obj = {
        "summary": f"{operation} the {table_name} table",
        "responses": {
            "200": {
                "description": "OK"
            }
        }
    }
    if method == 'GET':
        if '<id>' in rule_str:
            operation_obj["parameters"] = [
                {
                    "name": "id",
                    "in": "path",
                    "description": "The ID of the record to retrieve",
                    "required": True,
                    "schema": {
                        "type": primary_key_type,
                    }
                }
            ]
        else:
            add_paging_parameters(operation_obj)
    path_item[method.lower()] = operation_obj

def sqlite_type_to_openapi_type(sqlite_type):
    """
    Convert SQLite data types to OpenAPI data types.
    """
    sqlite_type = sqlite_type.upper()
    if sqlite_type in ["INT", "INTEGER", "TINYINT", "SMALLINT", "MEDIUMINT", "BIGINT", "UNSIGNED BIG INT", "INT2", "INT8"]:
        return "integer"
    elif sqlite_type in ["REAL", "DOUBLE", "DOUBLE PRECISION", "FLOAT"]:
        return "number"
    elif sqlite_type in ["TEXT", "CHARACTER", "VARCHAR", "VARYING CHARACTER", "NCHAR", "NATIVE CHARACTER", "NVARCHAR", "CLOB"]:
        return "string"
    elif sqlite_type in ["BLOB"]:
        return "string", "byte"
    elif sqlite_type in ["BOOLEAN"]:
        return "boolean"
    elif sqlite_type in ["DATE", "DATETIME"]:
        return "string", "date-time"
    else:
        return "string"

def generate_openapi_spec(db):
    # Basic OpenAPI spec
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "SQLite2REST",
            "version": __version__
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
                table_name = str(rule).split('/')[1]
                _, primary_key_type = db.get_primary_key(table_name)
                add_operation_to_path(path_item, method, str(rule), sqlite_type_to_openapi_type(primary_key_type))

    # Validate the spec
    validate_spec(spec)

    # Return the spec as a dictionary
    return spec

def get_openapi_spec(db):
    spec = generate_openapi_spec(db)
    return yaml.dump(spec)
