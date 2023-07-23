from flask import jsonify, request
from .database import Database
from .openapi import get_openapi_spec

def setup_routes(app, database_uri):
    tables = Database(database_uri).get_tables()

    def create_get_records_fn(table_name):
        def get_records():
            app.logger.info(f'Getting records for table {table_name}')
            records = Database(database_uri).get_records(table_name)
            return jsonify(records), 200, {'Content-Type': 'application/json'}
        get_records.__name__ = f'get_records_{table_name}'
        return get_records

    def create_create_record_fn(table_name):
        def create_record():
            data = request.get_json()
            app.logger.info(f'Creating record in table {table_name} with data {data}')
            Database(database_uri).create_record(table_name, data)
            return jsonify({'message': 'Record created.'}), 201, {'Content-Type': 'application/json'}
        create_record.__name__ = f'create_record_{table_name}'
        return create_record

    def create_update_record_fn(table_name):
        def update_record(id):
            data = request.get_json()
            app.logger.info(f'Updating record with id {id} in table {table_name} with data {data}')
            Database(database_uri).update_record(table_name, id, data)
            return jsonify({'message': 'Record updated.'}), 200, {'Content-Type': 'application/json'}
        update_record.__name__ = f'update_record_{table_name}'
        return update_record

    def create_delete_record_fn(table_name):
        def delete_record(id):
            app.logger.info(f'Deleting record with id {id} from table {table_name}')
            Database(database_uri).delete_record(table_name, id)
            return jsonify({'message': 'Record deleted.'}), 200, {'Content-Type': 'application/json'}
        delete_record.__name__ = f'delete_record_{table_name}'
        return delete_record

    for table_name in tables:
        app.add_url_rule(f'/{table_name}', 'get_records_'+table_name, create_get_records_fn(table_name), methods=['GET'])
        app.add_url_rule(f'/{table_name}', 'create_record_'+table_name, create_create_record_fn(table_name), methods=['POST'])
        app.add_url_rule(f'/{table_name}/<id>', 'update_record_'+table_name, create_update_record_fn(table_name), methods=['PUT'])
        app.add_url_rule(f'/{table_name}/<id>', 'delete_record_'+table_name, create_delete_record_fn(table_name), methods=['DELETE'])

    @app.route('/openapi.yaml', methods=['GET'])
    def openapi():
        app.logger.info('Getting OpenAPI specification')
        spec = get_openapi_spec()
        return spec, 200, {'Content-Type': 'text/vnd.yaml'}

