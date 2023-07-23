import unittest
from openapi_spec_validator import validate_spec
import yaml
from sqlite2rest import create_app

class TestOpenAPISpec(unittest.TestCase):
    def setUp(self):
        # Use a SQLite database file for testing
        self.app = create_app('data/chinook.db')
        self.client = self.app.test_client()

    def test_openapi_spec(self):
        response = self.client.get('/openapi.yaml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/vnd.yaml')

        # Load the spec as a dictionary
        spec = yaml.safe_load(response.data)

        # Validate the spec
        validate_spec(spec)

        # Check for the existence of the Artist endpoints
        self.assertIn('/Artist', spec['paths'])
        self.assertIn('/Artist/<id>', spec['paths'])

if __name__ == '__main__':
    unittest.main()
