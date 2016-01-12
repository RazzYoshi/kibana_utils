import unittest
import fabtest
import os
import fabfile

class fabFileTestCase(unittest.TestCase):
	
	def setUp(self):
		pass
	def tearDown(self):
		pass
	###Helper tests
	def test_get_path_returns_valid_path(self):
		filePath = fabtest._get_path()[0]
		self.assertTrue(os.path.exists(filePath))
	
	###Task tests
	
	
if __name__ == "__main__":
	unittest.main() # run all tests