from flask import jsonify, request
from .openapi import get_openapi_spec

def setup_routes(app, tables, get_database):
    def create_get_records_fn(table_name):
        def get_records():
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)
            app.logger.info(f'Getting records for table {table_name}, page {page}, {per_page} per page')
            records = get_database().get_records(table_name, page, per_page)
            return jsonify(records), 200, {'Content-Type': 'application/json'}
        get_records.__name__ = f'get_records_{table_name}'
        return get_records

    def create_get_record_fn(table_name):
        def get_record(id):
            app.logger.info(f'Getting record with id {id} from table {table_name}')
            record = get_database().get_record(table_name, id)
            if record is None:
                return jsonify({'message': 'Record not found.'}), 404, {'Content-Type': 'application/json'}
            return jsonify(record), 200, {'Content-Type': 'application/json'}
        get_record.__name__ = f'get_record_{table_name}'
        return get_record

    def create_create_record_fn(table_name):
        def create_record():
            data = request.get_json()
            app.logger.info(f'Creating record in table {table_name} with data {data}')
            get_database().create_record(table_name, data)
            return jsonify({'message': 'Record created.'}), 201, {'Content-Type': 'application/json'}
        create_record.__name__ = f'create_record_{table_name}'
        return create_record

    def create_update_record_fn(table_name):
        def update_record(id):
            data = request.get_json()
            app.logger.info(f'Updating record with id {id} in table {table_name} with data {data}')
            get_database().update_record(table_name, id, data)
            return jsonify({'message': 'Record updated.'}), 200, {'Content-Type': 'application/json'}
        update_record.__name__ = f'update_record_{table_name}'
        return update_record

    def create_delete_record_fn(table_name):
        def delete_record(id):
            app.logger.info(f'Deleting record with id {id} from table {table_name}')
            get_database().delete_record(table_name, id)
            return jsonify({'message': 'Record deleted.'}), 200, {'Content-Type': 'application/json'}
        delete_record.__name__ = f'delete_record_{table_name}'
        return delete_record

    for table_name in tables:
        app.add_url_rule(f'/{table_name}/<id>', 'get_record_'+table_name, create_get_record_fn(table_name), methods=['GET'])
        app.add_url_rule(f'/{table_name}', 'get_records_'+table_name, create_get_records_fn(table_name), methods=['GET'])
        app.add_url_rule(f'/{table_name}', 'create_record_'+table_name, create_create_record_fn(table_name), methods=['POST'])
        app.add_url_rule(f'/{table_name}/<id>', 'update_record_'+table_name, create_update_record_fn(table_name), methods=['PUT'])
        app.add_url_rule(f'/{table_name}/<id>', 'delete_record_'+table_name, create_delete_record_fn(table_name), methods=['DELETE'])

    @app.route('/openapi.yaml', methods=['GET'])
    def openapi():
        app.logger.info('Getting OpenAPI specification')
        spec = get_openapi_spec(get_database())
        return spec, 200, {'Content-Type': 'text/vnd.yaml'}

