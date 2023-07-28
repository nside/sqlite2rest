Usage
=====

To use SQLite2REST, you need to import it and create an app:

.. code-block:: python

   from sqlite2rest import create_app

   app = create_app('my_database.db')
   app.run()

This will start a Flask server with RESTful endpoints for each table in `my_database.db`.
