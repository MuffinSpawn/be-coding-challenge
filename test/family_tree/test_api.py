# -*- coding: utf-8 -*-
"""
Created on Wed Feb  27 08:23:49 2019

@author: peter
"""
import json
import logging
import os
import tempfile
import time
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from family_tree.app import create_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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

    def test_add_person(self):
        record = dict(first_name='Martin', last_name='McFly', birth_date='1972/9/15',
                      phone='708-555-4000', email='marty.mcfly@future.com',
                      address=dict(number='123', street='Sesame St.', city='New York', zipcode='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        person_id = response.json['id']
        self.assertEqual(1, person_id)

        response = self.client.get('api/person/1')
        self.assertTrue(response.json)
        self.assertDictEqual(record, response.json)

    def test_remove_person(self):
        pass

    def test_update_person(self):
        pass

    def test_add_child(self):
        record = dict(first_name='Martin', last_name='McFly', birth_date='1972/9/15',
                      phone='708-555-4000', email='marty.mcfly@future.com',
                      address=dict(number='123', street='Sesame St.', city='New York', zipcode='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        child_id = response.json['id']
        self.assertEqual(1, child_id)

        record = dict(first_name='George', last_name='McFly', birth_date='1942/2/23',
                      phone='708-555-4000', email='george.mcfly@future.com',
                      address=dict(number='123', street='Sesame St.', city='New York', zipcode='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        parent_id = response.json['id']
        self.assertEqual(2, parent_id)

        response = self.client.post('api/child/add/{}/{}'.format(parent_id, child_id))
        self.assertEqual(200, response.status_code)

        response = self.client.get('api/children/{}'.format(parent_id))
        child_ids = response.json
        self.assertEqual(1, len(child_ids))
        self.assertEqual(child_id, child_ids[0])

    def test_find_siblings(self):
        record = dict(first_name='Martin', last_name='McFly', birth_date='1972/9/15',
                      phone='708-555-4000', email='marty.mcfly@future.com',
                      address=dict(number='123', street='Sesame St.', city='New York', zipcode='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        brother_id = response.json['id']
        self.assertEqual(1, brother_id)

        record = dict(first_name='George', last_name='McFly', birth_date='1942/2/23',
                      phone='708-555-4000', email='george.mcfly@future.com',
                      address=dict(number='123', street='Sesame St.', city='New York', zipcode='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        parent_id = response.json['id']
        self.assertEqual(2, parent_id)

        response = self.client.post('api/child/add/{}/{}'.format(parent_id, brother_id))
        self.assertEqual(200, response.status_code)

        record = dict(first_name='Mandy', last_name='McFly', birth_date='1970/02/03',
                      phone='708-555-4000', email='mandy.mcfly@future.com',
                      address=dict(number='123', street='Sesame St.', city='New York', zipcode='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        sister_id = response.json['id']
        self.assertEqual(3, sister_id)

        response = self.client.post('api/child/add/{}/{}'.format(parent_id, sister_id))
        self.assertEqual(200, response.status_code)

        response = self.client.get('api/siblings/{}'.format(brother_id))
        sibling_ids = response.json
        self.assertEqual(2, len(sibling_ids))
        self.assertTrue(sister_id in sibling_ids)
        self.assertTrue(brother_id in sibling_ids)

    def test_find_parents(self):
        pass

    def test_find_grandparents(self):
        pass

    def test_find_cousings(self):
        pass

if __name__ == '__main__':
    unittest.main()