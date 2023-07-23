import unittest
import json
import os
import shutil
from sqlite2rest import create_app

class TestRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Copy the database file before running the tests
        shutil.copyfile('data/chinook.db', 'test_chinook.db')

    @classmethod
    def tearDownClass(cls):
        # Delete the copied database file after running the tests
        os.remove('test_chinook.db')

    def setUp(self):
        # Use the copied database file for testing
        self.app = create_app('test_chinook.db')
        self.client = self.app.test_client()

    def test_get(self):
        response = self.client.get('/Artist')
        self.assertEqual(response.status_code, 200)
        artists = json.loads(response.data)
        self.assertIsInstance(artists, list)

    def test_create(self):
        response = self.client.post('/Artist', json={'Name': 'Test Artist'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data), {'message': 'Record created.'})

    def test_update(self):
        # First, create a record to update
        self.client.post('/Artist', json={'Name': 'Test Artist'})

        # Then, update the record
        response = self.client.put('/Artist/1', json={'Name': 'Updated Artist'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'message': 'Record updated.'})

    def test_delete(self):
        # First, create a record to delete
        self.client.post('/Artist', json={'Name': 'Test Artist'})

        # Then, delete the record
        response = self.client.delete('/Artist/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'message': 'Record deleted.'})

if __name__ == '__main__':
    unittest.main()
