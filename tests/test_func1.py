import unittest
from unittest import mock
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from src import func1

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'url_valid':
        return MockResponse({"key1": "value1"}, 200)

    return MockResponse({}, 404)


class TestFunction1(unittest.TestCase):
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_lambda_handler_ok(self, mock_get):
        res = func1.lambda_handler({'url': 'url_valid'}, ' ')
        self.assertEqual(res, {"key1": "value1"})

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_lambda_handler_ng(self, mock_get):
        res = func1.lambda_handler({'url': 'url_invalid'}, ' ')
        self.assertEqual(res, 404)


if __name__ == '__main__':
    unittest.main()
