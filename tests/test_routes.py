import json
import os
from sqlite2rest import Database, create_app
import unittest

class TestRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a database file for testing
        cls.db_uri = 'test.db'
        cls.db = Database(cls.db_uri)

        # Create a test table
        cls.db.cursor.execute('CREATE TABLE Artist (ArtistId INTEGER PRIMARY KEY, Name TEXT);')
        cls.db.conn.commit()

    @classmethod
    def tearDownClass(cls):
        # Delete the database file after running the tests
        os.remove('test.db')

    def setUp(self):
        # Create the Flask app
        self.app = create_app(self.db_uri)
        self.client = self.app.test_client()

    def test_0get(self):
        response = self.client.get('/Artist')
        self.assertEqual(response.status_code, 200)
        artists = json.loads(response.data)
        self.assertIsInstance(artists, list)
        self.assertEqual(artists, [])

    def test_create(self):
        response = self.client.post('/Artist', json={'ArtistId': 1, 'Name': 'Test Artist'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data), {'message': 'Record created.'})

        # Verify the creation by reading it back
        response = self.client.get('/Artist')
        self.assertEqual(response.status_code, 200)
        artists = json.loads(response.data)
        self.assertEqual(artists, [{'ArtistId': 1, 'Name': 'Test Artist'}])

    def test_update(self):
        # First, create a record to update
        self.client.post('/Artist', json={'ArtistId': 2, 'Name': 'Test Artist'})

        # Then, update the record
        response = self.client.put('/Artist/2', json={'Name': 'Updated Artist'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'message': 'Record updated.'})

    def test_delete(self):
        # First, create a record to delete
        self.client.post('/Artist', json={'ArtistId': 3, 'Name': 'Test Artist'})

        # Then, delete the record
        response = self.client.delete('/Artist/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'message': 'Record deleted.'})

    def test_get_single_record(self):
        # First, create a record to get
        self.client.post('/Artist', json={'ArtistId': 4, 'Name': 'Test Artist'})

        # Then, get the record
        response = self.client.get('/Artist/4')
        self.assertEqual(response.status_code, 200)
        artist = json.loads(response.data)
        self.assertEqual(artist, {'ArtistId': 4, 'Name': 'Test Artist'})

    def test_get_single_record_not_found(self):
        # Try to get a record that does not exist
        response = self.client.get('/Artist/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data), {'message': 'Record not found.'})
