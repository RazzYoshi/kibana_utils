
import unittest

import os
import fabfile

import boto
import boto.s3
from boto.s3.key import Key

import datetime

import mock
from mock import patch
from mock import MagicMock

import requests

import json

def _get_path():
    HOME_PATH = os.environ['HOME']
    OTHER_PATH = os.environ['HOME']
    return [HOME_PATH, OTHER_PATH]
    
def _compare_paths():
    HOME_PATH = _get_path()[0]
    OTHER_PATH = _get_path()[1]
    print (HOME_PATH == OTHER_PATH)
    
def main():
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'asdf'
    os.environ['AWS_ACCESS_KEY_ID'] = 'candycane'
    
    os.environ['KIBANA_BUCKET'] = 'my-bucket'
    os.environ['KIBANA_PREFIX'] = 'kibana-backup'

    os.environ['ELASTIC_SEARCH_HOST'] = '127.0.02'
    os.environ['ELASTIC_SEARCH_PORT'] = '9292'

    data = json.loads('{"_source":1}')
    ret = data['_source']
    print ret
    print type(ret)
    #fabfile._get_dashboard = MagicMock(return_value=)
    #var = fabfile._get_dashboard(7)

    #print type(var)

if __name__ == "__main__":
    main()
