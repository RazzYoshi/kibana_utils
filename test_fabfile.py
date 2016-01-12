import unittest
import fabfile
import os
import boto
import datetime
import requests

class fabFileTestCase(unittest.TestCase):
    
    def setUp(self):
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'asdf'
        os.environ['AWS_ACCESS_KEY_ID'] = 'candycane'
        
        os.environ['KIBANA_BUCKET'] = 'my-bucket'
        os.environ['KIBANA_PREFIX'] = 'kibana-backups'

    def tearDown(self):
        pass
    
    ###Helper tests
    def test__get_s3_bucket_vars_returns_array_size_two(self):
        mockreturnlength = fabfile._get_s3_bucket_vars().__len__()
        self.assertEquals(mockreturnlength,2)

    def test__get_s3_bucket_vars_returns_correct_array(self):
        mockreturn = fabfile._get_s3_bucket_vars()
        self.assertEquals(mockreturn[0],'my-bucket')
        self.assertEquals(mockreturn[1],'kibana-backups')

    def test_es_url_should_return_valid_url(self):
        mockURL = fabfile._es_url('mock')
        self.assertRegexpMatches(mockURL, "http://")

    def test_get_boto_connection_returns_valid_connection(self):
        mockconnection = fabfile._get_boto_connection()
        self.assertIsInstance(mockconnection, boto.s3.connection.S3Connection)
    
    def test_get_backup_key_return_is_json(self):
        mockbkupkey = fabfile._get_backup_key('string')
        self.assertRegexpMatches(mockbkupkey, ".json")

    def test__get_backup_key_return_has_bucket_prefix(self):
        bucket_prefix= os.environ['KIBANA_PREFIX']
        mockbkupkey = fabfile._get_backup_key('string')
        self.assertRegexpMatches(mockbkupkey, bucket_prefix)

    def test__get_time_string_returns_datetime_now(self):
        mocktime = fabfile._get_time_string('%c')
        truetime = datetime.datetime.now().strftime('%c').lower()
        self.assertTrue(mocktime == truetime)

    ###Task tests
    
    
if __name__ == "__main__":
    unittest.main() # run all tests