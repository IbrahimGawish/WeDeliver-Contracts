import unittest
from app import app


class FlaskApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_hello_endpoint(self):
        response = self.app.get("/api/sayHello")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "Hello, Welcome to Contract Service")

    def test_index_endpoint(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_get_current_contracts(self):
        response = self.app.get("/api/get_current_contracts")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
