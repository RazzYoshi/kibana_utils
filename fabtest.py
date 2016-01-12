
import unittest

import os
import fabfile

import boto
import boto.s3
from boto.s3.key import Key

import datetime

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

	print fabfile._get_dashboards()


if __name__ == "__main__":
	main()
