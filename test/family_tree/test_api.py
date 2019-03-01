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
                      address=dict(number='123', street='Sesame St.', city='New York', postal_code='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        self.assertEqual(201, response.status_code)
        person_id = response.json['id']
        self.assertEqual(1, person_id)

        response = self.client.get('api/person/1')
        self.assertTrue(response.json)
        self.assertDictEqual(record, response.json)

    def test_remove_person(self):
        record = dict(first_name='Martin', last_name='McFly', birth_date='1972/9/15',
                      phone='708-555-4000', email='marty.mcfly@future.com',
                      address=dict(number='123', street='Sesame St.', city='New York', postal_code='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        self.assertEqual(201, response.status_code)
        child_id = response.json['id']

        record = dict(first_name='George', last_name='McFly', birth_date='1942/2/23',
                      phone='708-555-4000', email='george.mcfly@future.com',
                      address=dict(number='123', street='Sesame St.', city='New York', postal_code='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        self.assertEqual(201, response.status_code)
        parent_id = response.json['id']

        response = self.client.post('api/child/add/{}/{}'.format(parent_id, child_id))
        self.assertEqual(200, response.status_code)

        response = self.client.post('api/person/remove/{}'.format(child_id))
        self.assertEqual(200, response.status_code)

        response = self.client.get('api/children/{}'.format(parent_id))
        self.assertEqual(200, response.status_code)

        response = self.client.get('api/person/1')
        self.assertEqual(404, response.status_code)

        response = self.client.get('api/children/{}'.format(parent_id))
        self.assertEqual(200, response.status_code)
        child_ids = response.json
        self.assertEqual(0, len(child_ids))

        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        self.assertEqual(201, response.status_code)
        child_id = response.json['id']

        response = self.client.post('api/child/add/{}/{}'.format(parent_id, child_id))
        self.assertEqual(200, response.status_code)

        response = self.client.post('api/person/remove/{}'.format(parent_id))
        self.assertEqual(200, response.status_code)

        response = self.client.get('api/parents/{}'.format(child_id))
        self.assertEqual(200, response.status_code)
        parent_ids = response.json
        self.assertEqual(0, len(parent_ids))


    def test_update_person(self):
        record = dict(first_name='Martin', last_name='McFly', birth_date='1972/9/15',
                      phone='708-555-4000', email='marty.mcfly@future.com',
                      address=dict(number='123', street='Sesame St.', city='New York', postal_code='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        self.assertEqual(201, response.status_code)
        person_id = response.json['id']
        self.assertEqual(1, person_id)

        response = self.client.get('api/person/1')
        self.assertEqual('708-555-4000', response.json['phone'])

        # Update phone number
        update_record = dict(phone='630-555-9258')
        response = self.client.post('api/person/update/{}'.format(person_id), data=json.dumps(update_record),
                                    headers={'content-type':'application/json'})
        self.assertEqual(200, response.status_code)

        response = self.client.get('api/person/1')
        self.assertEqual(update_record['phone'], response.json['phone'])

        # Update address
        update_record = dict(address=dict(number='221B', street='Baker St.', city='London', postal_code='WC2N 5DU', country='UK'))
        response = self.client.post('api/person/update/{}'.format(person_id), data=json.dumps(update_record),
                                    headers={'content-type':'application/json'})
        self.assertEqual(200, response.status_code)

        response = self.client.get('api/person/1')
        self.assertDictEqual(update_record['address'], response.json['address'])


    def test_add_child(self):
        record = dict(first_name='Martin', last_name='McFly', birth_date='1972/9/15',
                      phone='708-555-4000', email='marty.mcfly@future.com',
                      address=dict(number='123', street='Sesame St.', city='New York', postal_code='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        self.assertEqual(201, response.status_code)
        child_id = response.json['id']
        self.assertEqual(1, child_id)

        record = dict(first_name='George', last_name='McFly', birth_date='1942/2/23',
                      phone='708-555-4000', email='george.mcfly@future.com',
                      address=dict(number='123', street='Sesame St.', city='New York', postal_code='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        self.assertEqual(201, response.status_code)
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
                      address=dict(number='123', street='Sesame St.', city='New York', postal_code='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        self.assertEqual(201, response.status_code)
        brother_id = response.json['id']
        self.assertEqual(1, brother_id)

        record = dict(first_name='George', last_name='McFly', birth_date='1942/2/23',
                      phone='708-555-4000', email='george.mcfly@future.com',
                      address=dict(number='123', street='Sesame St.', city='New York', postal_code='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        self.assertEqual(201, response.status_code)
        parent_id = response.json['id']
        self.assertEqual(2, parent_id)

        response = self.client.post('api/child/add/{}/{}'.format(parent_id, brother_id))
        self.assertEqual(200, response.status_code)

        record = dict(first_name='Mandy', last_name='McFly', birth_date='1970/02/03',
                      phone='708-555-4000', email='mandy.mcfly@future.com',
                      address=dict(number='123', street='Sesame St.', city='New York', postal_code='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        self.assertEqual(201, response.status_code)
        sister_id = response.json['id']
        self.assertEqual(3, sister_id)

        response = self.client.post('api/child/add/{}/{}'.format(parent_id, sister_id))
        self.assertEqual(200, response.status_code)

        response = self.client.get('api/siblings/{}'.format(brother_id))
        self.assertEqual(200, response.status_code)
        sibling_ids = response.json
        self.assertEqual(1, len(sibling_ids))
        self.assertTrue(sister_id in sibling_ids)

    def test_find_parents(self):
        record = dict(first_name='Martin', last_name='McFly', birth_date='1972/9/15',
                      phone='708-555-4000', email='marty.mcfly@future.com',
                      address=dict(number='123', street='Sesame St.', city='New York', postal_code='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        self.assertEqual(201, response.status_code)
        child_id = response.json['id']
        self.assertEqual(1, child_id)

        record = dict(first_name='George', last_name='McFly', birth_date='1942/2/23',
                      phone='708-555-4000', email='george.mcfly@future.com',
                      address=dict(number='123', street='Sesame St.', city='New York', postal_code='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        self.assertEqual(201, response.status_code)
        father_id = response.json['id']
        self.assertEqual(2, father_id)

        response = self.client.post('api/child/add/{}/{}'.format(father_id, child_id))
        self.assertEqual(200, response.status_code)

        record = dict(first_name='Lorraine', last_name='McFly', birth_date='1942/5/04',
                      phone='708-555-4000', email='lorraine.mcfly@future.com',
                      address=dict(number='123', street='Sesame St.', city='New York', postal_code='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        self.assertEqual(201, response.status_code)
        mother_id = response.json['id']
        self.assertEqual(3, mother_id)

        response = self.client.post('api/child/add/{}/{}'.format(mother_id, child_id))
        self.assertEqual(200, response.status_code)

        response = self.client.get('api/parents/{}'.format(child_id))
        self.assertEqual(200, response.status_code)
        parent_ids = response.json
        self.assertEqual(2, len(parent_ids))
        self.assertTrue(mother_id in parent_ids)
        self.assertTrue(father_id in parent_ids)

    def test_find_grandparents(self):
        record = dict(first_name='Martin', last_name='McFly', birth_date='1972/9/15',
                      phone='708-555-4000', email='marty.mcfly@future.com',
                      address=dict(number='123', street='Sesame St.', city='New York', postal_code='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        self.assertEqual(201, response.status_code)
        child_id = response.json['id']
        self.assertEqual(1, child_id)

        record = dict(first_name='George', last_name='McFly', birth_date='1942/02/23',
                      phone='708-555-4000', email='george.mcfly@future.com',
                      address=dict(number='123', street='Sesame St.', city='New York', postal_code='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        self.assertEqual(201, response.status_code)
        father_id = response.json['id']
        self.assertEqual(2, father_id)

        response = self.client.post('api/child/add/{}/{}'.format(father_id, child_id))
        self.assertEqual(200, response.status_code)

        record = dict(first_name='Mary', last_name='McFly', birth_date='1920/07/11',
                      phone='915-555-1234', email='mary.mcfly@future.com',
                      address=dict(number='999', street='Meadow Ln.', city='Falls Church', postal_code='03124', country='USA'))
        response = self.client.post('api/person/add', data=json.dumps(record),
                                    headers={'content-type':'application/json'})
        self.assertEqual(201, response.status_code)
        grandmother_id = response.json['id']
        self.assertEqual(3, grandmother_id)

        response = self.client.post('api/child/add/{}/{}'.format(grandmother_id, father_id))
        self.assertEqual(200, response.status_code)

        response = self.client.get('api/grandparents/{}'.format(child_id))
        self.assertEqual(200, response.status_code)
        grandparent_ids = response.json
        self.assertEqual(1, len(grandparent_ids))
        self.assertEqual(grandmother_id, grandparent_ids[0])

    def test_find_cousins(self):
        pass

if __name__ == '__main__':
    unittest.main()