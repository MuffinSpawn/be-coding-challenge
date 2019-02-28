# -*- coding: utf-8 -*-
"""
Created on Wed Feb  27 08:23:49 2019

@author: peter
"""
import json
import logging
import os
import requests
import tempfile
import time
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from family_tree.app import create_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# class FamilyTreeClient():
#     def __init__(self, base_url=None):
#         self.base_url = base_url
#         if not self.base_url:
#             self.base_url = 'http://127.0.0.1:5000'

#     def _get(self, id, rest_path):
#         response = requests.get('{}/{}/{}'.format(self.base_url, rest_path, id))
#         if response.status_code != 200:
#             return None
#         return response.json()

#     def get_person(self, id):
#         return self._get(id, 'person')

#     def get_parents(self, id):
#         return self._get(id, 'relative/parents')

#     def get_children(self, id):
#         return self._get(id, 'relative/children')

#     def get_grandparents(self, id):
#         return self._get(id, 'relative/grandparents')

#     def get_siblings(self, id):
#         return self._get(id, 'relative/siblings')

#     def get_cousins(self, id):
#         return self._get(id, 'relative/cousins')

#     def insert_person(self, name, birth_date, phone, email, address):
#         record = dict(name=name, phone=phone, email=email, address=address)
#         response = requests.put('{}/person/add'.format(self.base_url), data=record)
#         return response.status_code

#     def set_parent(self, child_id, parent_id):
#         record = dict(child_id=child_id, parent_id=parent_id)
#         response = requests.put('{}/relative/parent'.format(self.base_url), data=record)
#         return response.status_code

#     def set_child(self, parent_id, child_id):
#         record = dict(child_id=child_id, parent_id=parent_id)
#         response = requests.put('{}/relative/child'.format(self.base_url), data=record)
#         return response.status_code

# Base class for most of the other test cases. Used to setup and teardown
# the LTSimulator instance that the test cases use.
class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.db_file,self.db_path = tempfile.mkstemp(suffix='.db')

        self.app = create_app(config=dict(TESTING=True), db_path=self.db_path)
        self.app.config['db'].create()

        self.client = self.app.test_client()

    def tearDown(self):
        self.app.config['db'].close()
        os.close(self.db_file)
        os.remove(self.db_path)
    
    def test_health_check(self):
        response = self.client.get('api/health_check')
        healthy = response.json
        self.assertTrue(healthy)

    def test_insert_person(self):
        pass

    def test_add_relationship(self):
        pass

    def test_remove_relationship(self):
        pass

    def test_remove_person(self):
        pass

    def test_update_person(self):
        pass

    def test_person(self):
        record = dict(first_name='Peter', last_name='Lane', birth_date='1972/9/15',
                      phone='708-555-4000', email='marty.mcfly@future.com',
                      address=dict(number=123, street='Sesame St.', city='New York', zipcode='03124', country='USA'))
        logger.debug(self.client.post.__doc__)
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        self.assertDictEqual(response.json, dict(id=1))

        response = self.client.get('api/person/1')
        self.assertTrue(response.json)
        logger.debug('Response: {}'.format(response))

    def test_find_relatives(self):
        pass

if __name__ == '__main__':
    unittest.main()