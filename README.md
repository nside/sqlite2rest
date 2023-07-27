# SQLite2REST

SQLite2REST is a Python library that simplifies the process of creating a RESTful API from an SQLite database using the Flask web framework. It automatically reads the schema of an SQLite database and generates endpoints for each table, allowing for Create, Read, Update, and Delete (CRUD) operations. The library also generates an OpenAPI specification for the API.

![Test status](https://img.shields.io/github/actions/workflow/status/nside/sqlite2rest/test.yaml)

## Installation

You can install SQLite2REST using pip:

```
pip install sqlite2rest
```


## Usage

You can use SQLite2REST from the command line by providing the path to your SQLite database:

```
sqlite2rest /path/to/database.db
```


This will start a Flask server with endpoints for each table in the database. For example, if your database has a table named `users`, you can access the records in this table at the `/users` endpoint.

You can also use the `/openapi.yaml` endpoint to get the OpenAPI specification for the API.

## Endpoints

For each table in the database, the following endpoints are available:

- `GET /<table>`: Get all records from the table.
- `GET /<table>/<id>`: Returns the record with the given ID from the table.
- `POST /<table>`: Create a new record in the table. The data for the record should be provided as JSON in the request body.
- `PUT /<table>/<id>`: Update an existing record in the table. The data for the record should be provided as JSON in the request body.
- `DELETE /<table>/<id>`: Delete an existing record from the table.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

SQLite2REST is licensed under the MIT license. See the LICENSE file for more details.

