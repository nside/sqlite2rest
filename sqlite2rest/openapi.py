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

def add_operation_to_path(path_item, method, rule_str, primary_key_type, schema):
    operation = get_operation_summary(method)
    table_name = rule_str.split('/')[1]
    operation_obj = {
        "summary": f"{operation} the {table_name} table",
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
            add_response_to_operation(operation_obj, schema)
        else:
            add_paging_parameters(operation_obj)
            add_response_to_operation(operation_obj, {"type": "array", "items": schema})
    elif method == 'POST':
        operation_obj["requestBody"] = {
            "content": {
                "application/json": {
                    "schema": schema
                }
            }
        }
        add_response_to_operation(operation_obj, schema)
    elif method == 'PUT':
        operation_obj["parameters"] = [
            {
                "name": "id",
                "in": "path",
                "description": "The ID of the record to update",
                "required": True,
                "schema": {
                    "type": primary_key_type,
                }
            }
        ]
        operation_obj["requestBody"] = {
            "content": {
                "application/json": {
                    "schema": schema
                }
            }
        }
        add_response_to_operation(operation_obj, schema)
    elif method == 'DELETE':
        operation_obj["parameters"] = [
            {
                "name": "id",
                "in": "path",
                "description": "The ID of the record to delete",
                "required": True,
                "schema": {
                    "type": primary_key_type,
                }
            }
        ]
        operation_obj["responses"] = {
            "200": {
                "description": "OK"
            }
        }
    path_item[method.lower()] = operation_obj

def add_response_to_operation(operation_obj, schema):
    operation_obj["responses"] = {
        "200": {
            "description": "OK",
            "content": {
                "application/json": {
                    "schema": schema
                }
            }
        }
    }

def sqlite_type_to_openapi_type(sqlite_type):
    """
    Convert SQLite data types to OpenAPI data types.
    """
    sqlite_type = sqlite_type.upper()
    if sqlite_type in ["INT", "INTEGER", "TINYINT", "SMALLINT", "MEDIUMINT", "BIGINT", "UNSIGNED BIG INT", "INT2", "INT8"]:
        return "integer"
    elif sqlite_type in ["REAL", "DOUBLE", "DOUBLE PRECISION", "FLOAT"]:
        return "number"
    elif sqlite_type in ["TEXT", "CHARACTER", "VARCHAR", "VARYING CHARACTER", "NCHAR", "NATIVE CHARACTER", "CLOB"]:
        return "string"
    elif sqlite_type.startswith("NVARCHAR"):
        return "string"
    elif sqlite_type in ["BLOB"]:
        return "byte"
    elif sqlite_type in ["BOOLEAN"]:
        return "boolean"
    elif sqlite_type in ["DATE", "DATETIME"]:
        return "string"
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
        "paths": {},
        "components": {
            "schemas": {}
        }
    }

    # Generate schemas for each table
    spec["components"] = {"schemas": {}}
    for table_name in db.get_tables():
        schema = db.get_table_schema(table_name)
        spec["components"]["schemas"][table_name] = {
            "type": "object",
            "properties": {column: {"type": sqlite_type_to_openapi_type(sqlite_type)} for column, sqlite_type in schema.items()}
        }

    # Generate paths for each table
    for table_name in db.get_tables():
        # Get the primary key and schema for the table
        _, primary_key_type = db.get_primary_key(table_name)
        primary_key_type = sqlite_type_to_openapi_type(primary_key_type)
        schema = spec["components"]["schemas"][table_name]

        # Add the GET (all records), POST, PUT, and DELETE operations for the table
        path_item = spec["paths"].setdefault(f'/{table_name}', {})
        add_operation_to_path(path_item, 'GET', f'/{table_name}', primary_key_type, schema)
        add_operation_to_path(path_item, 'POST', f'/{table_name}', primary_key_type, schema)

        # Add the GET (single record), PUT, and DELETE operations for a record in the table
        path_item = spec["paths"].setdefault(f'/{table_name}/<id>', {})
        add_operation_to_path(path_item, 'GET', f'/{table_name}/<id>', primary_key_type, schema)
        add_operation_to_path(path_item, 'PUT', f'/{table_name}/<id>', primary_key_type, schema)
        add_operation_to_path(path_item, 'DELETE', f'/{table_name}/<id>', primary_key_type, schema)

    # Validate the spec
    validate_spec(spec)

    # Return the spec as a dictionary
    return spec

def get_openapi_spec(db):
    spec = generate_openapi_spec(db)
    return yaml.dump(spec)
