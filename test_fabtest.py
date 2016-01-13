import unittest
import fabtest
import os
import fabfile

import mock
from mock import patch

import requests

class fabFileTestCase(unittest.TestCase):
    
    def setUp(self):
        pass
    def tearDown(self):
        pass
    ###Helper tests
    def test_get_path_returns_valid_path(self):
        filePath = fabtest._get_path()[0]
        self.assertTrue(os.path.exists(filePath))
    
    @patch('requests.get')
    def test_requests_get_called(self, requests_get):
        fabfile._get_dashboards()
        self.assertTrue(requests_get.called)

    ###Task tests
    
    
if __name__ == "__main__":
    unittest.main() # run all tests