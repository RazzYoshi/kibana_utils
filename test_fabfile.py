import unittest
import fabfile
import os
import boto
import datetime
import requests
import json

import dateutil

import mock
from mock import patch

class fabFileTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'asdf'
        os.environ['AWS_ACCESS_KEY_ID'] = 'candycane'
        
        os.environ['KIBANA_BUCKET'] = 'my-bucket'
        os.environ['KIBANA_PREFIX'] = 'kibana-backups'

    def tearDown(self):
        pass
    
    ###Helper tests
    #__get_s3_bucket_vars()
    def test__get_s3_bucket_vars_returns_array_size_two(self):
        mockreturnlength = fabfile._get_s3_bucket_vars().__len__()
        self.assertEquals(mockreturnlength,2)

    #__get_s3_bucket_vars()
    def test__get_s3_bucket_vars_returns_correct_array(self):
        mockreturn = fabfile._get_s3_bucket_vars()
        self.assertEquals(mockreturn[0],'my-bucket')
        self.assertEquals(mockreturn[1],'kibana-backups')

    #__es_url()
    def test_es_url_should_return_valid_url(self):
        mockURL = fabfile._es_url('mock')
        self.assertRegexpMatches(mockURL, "http://")

    #__get_boto_connection()
    def test_get_boto_connection_returns_valid_connection(self):
        mockconnection = fabfile._get_boto_connection()
        self.assertIsInstance(mockconnection, boto.s3.connection.S3Connection)
    
    #__get_backup_key()
    def test_get_backup_key_return_is_json(self):
        mockbkupkey = fabfile._get_backup_key('string')
        self.assertRegexpMatches(mockbkupkey, ".json")

    #__get_backup_key()
    def test__get_backup_key_return_contains_bucket_prefix(self):
        bucket_prefix= os.environ['KIBANA_PREFIX']
        mockbkupkey = fabfile._get_backup_key('string')
        self.assertRegexpMatches(mockbkupkey, bucket_prefix)

    #_get_time_string()
    def test__get_time_string_returns_datetime_now(self):
        mocktime = fabfile._get_time_string('%c')
        truetime = datetime.datetime.now().strftime('%c').lower()
        self.assertTrue(mocktime == truetime)

    #_get_dashboards()
    @patch('requests.get')
    def test_get_dashboards_calls_requests_get(self, requests_get):
        fabfile._get_dashboards()
        self.assertTrue(requests_get.called)

    #_get_dashboard()
    @patch('requests.get')
    @patch('json.loads')
    def test_get_dashboard_calls_json_loads(self, requests_get, json_loads):
        fabfile._get_dashboard(7)
        self.assertTrue(json_loads.called)

    #_get_dashboard()
    @patch('requests.get')
    @patch('json.loads', return_value={"_source":1})
    def test_get_dashboard_returns_data_at_key_source(self, requests_get, json_loads):
        dashboard = fabfile._get_dashboard(7)
        self.assertEquals(dashboard,1)

    #_create_dashboard()
    @patch('requests.put')
    def test_create_dashboard_calls_requests_put(self, requests_put):
        with self.assertRaises(Exception) as raised_exception:
            fabfile._create_dashboard(7,{"_source":1})
        self.assertTrue(requests_put.called)

    #_convert_dashboard_v0_v1()
    def test_convert_dashboard_v0_v1_correctly_removes_fields(self):
        mockstring = fabfile._convert_dashboard_v0_v1('{"_source":1,"@fields._name":2}')
        self.assertEquals(mockstring, '{"_source":1,"_name":2}')

    #_get_backup_object()
    @patch('fabfile._get_boto_connection')
    def test_get_backup_object_calls_get_boto_connection(self, get_boto_connection):
        fabfile._get_backup_object(1)
        self.assertTrue(get_boto_connection.called)

    #_get_backup_objects()
    @patch('fabfile._get_boto_connection')
    def test_get_backup_objects_calls_get_boto_connection(self, get_boto_connection):
        fabfile._get_backup_objects()
        self.assertTrue(get_boto_connection.called)

    #_do_backup()
    @patch('fabfile._get_boto_connection')
    @patch('fabfile._get_dashboards')
    def test_do_backup_calls_get_dashboards(self, get_boto_connection, get_dashboards):
        fabfile._do_backup(['a','b','c'])
        self.assertTrue(get_dashboards.called)

    ###Task tests
    #verify_backups()
    @patch('dateutil.parser.parse')
    @patch('fabfile._get_boto_connection')
    def test_verify_backups_calls_parser_parse(self, parser_parse, get_boto_connection):
        with self.assertRaises(SystemExit) as system_exit:
            fabfile.verify_backups()
        self.assertTrue(parser_parse.called)

    #delete_dashboards()
    @patch('requests.get')
    @patch('requests.delete')
    @patch('fabfile._get_dashboards', return_value= '{"hits":{"hits":[{"_id":1,"_source":"com.google"},{"_id":2,"_source":"io.pantheon"}]}}')
    def test_delete_dashboards_calls_requests_delete(self, requests_get, requests_delete, get_dashboards):
        fabfile.delete_dashboards()
        self.assertTrue(requests_delete.called)
    
    #needs refactoring, actual coverage smaller than intended
    #restore_dashboards()
    @patch('requests.post')
    @patch('fabfile._get_boto_connection')
    def test_restore_dashboards_calls_requests_post_attempt(self, requests_post, get_boto_connection):
        def mock_get_contents_as_string(self):
            return '{"hits":{"hits":[{"_id":1,"_source":"com.google"},{"_id":2,"_source":"io.pantheon"}]}}'

        mock_backup_object = mock.Mock('fabfile._get_backup_object')
        mock_backup_object.get_contents_as_string = mock_get_contents_as_string

        fabfile.restore_dashboards(1)
        self.assertTrue(requests_post.called)

    #export_dashboard()
    @patch('json.dumps', return_value= '{"_source":1}')
    @patch('requests.get')
    @patch('fabfile._get_dashboard')
    def test_export_dashboard_calls_json_dumps(self, json_dumps, requests_get, get_dashboard):
        fabfile.export_dashboard("pantheon","pantheon.txt")
        self.assertTrue(json_dumps.called)

    #import_dashboard()
    @patch('json.loads')
    @patch('requests.get')
    @patch('fabfile._create_dashboard')
    def test_import_dashboard_calls_json_loads(self, json_loads, requests_get, create_dashboard):
        fabfile.import_dashboard("pantheon","pantheon.txt")
        self.assertTrue(json_loads.called)

    #convert_dashboard_v0_v1()
    @patch('fabfile._convert_dashboard_v0_v1', return_value="pantheor")
    def test_convert_dashboard_v0_v1_calls_convert_dashboard_v0_v1_helper(self, convert_dashboard_v0_v1):
        fabfile.convert_dashboard_v0_v1("pantheon.txt","pantheonio.txt")
        self.assertTrue(convert_dashboard_v0_v1.called)

    #list_dashboards()
    @patch('json.loads')
    @patch('requests.get')
    def test_list_dashboards_calls_json_loads(self, json_loads, requests_get):
        fabfile.list_dashboards()
        self.assertTrue(json_loads.called)

    #list_backups()
    @patch('fabfile._get_backup_object')
    @patch('fabfile._get_boto_connection')
    def test_list_backups_calls_get_backup_object(self, get_backup_object, get_boto_connection):
        fabfile.list_backups()
        self.assertTrue(get_backup_object.called)

    #print_backup()
    @patch('fabfile._get_backup_object')
    def test_print_backup_calls_get_backup_object(self, get_backup_object):
        def mock_get_contents_as_string(self):
            return '{"hits":{"hits":[{"_id":1,"_source":"com.google"},{"_id":2,"_source":"io.pantheon"}]}}'

        mock_backup_object = mock.Mock('fabfile._get_backup_object')
        mock_backup_object.get_contents_as_string = mock_get_contents_as_string

        fabfile.print_backup(1)
        self.assertTrue(get_backup_object.called)

    #backup()
    @patch('fabfile._get_dashboards')
    @patch('fabfile._get_boto_connection')
    def test_backup_calls_get_dashboards(self, get_dashboards, get_boto_connection):
        fabfile.backup()
        self.assertTrue(get_dashboards.called)

if __name__ == "__main__":
    unittest.main() # run all tests