# -*- coding: utf-8 -*-
"""
Created on Wed Feb  27 08:23:49 2019

@author: peter
"""
import logging
import requests
import time
import unittest

from family_tree import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FamilyTreeClient():
    def __init__(self, url):
        self.client = None

    def insert_person(self, record):
        # Validate record dict
        # Insert Person
        # Insert Address

# Base class for most of the other test cases. Used to setup and teardown
# the LTSimulator instance that the test cases use.
class ApiTestCase(unittest.TestCase):
    db_path = 'test.db'

    def setUp(self):
        db.create(ApiTestCase.db)

    def tearDown(self):
        db.delete(ApiTestCase.db)

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

    def test_find(self):
        pass

if __name__ == '__main__':
    unittest.main()