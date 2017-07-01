#!/usr/bin/env python2
# -*- coding: utf8 -*-

import app as app
import os, time
import unittest
import flask


class TestCase(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
	self.app = app.app.test_client()	
        pass

    def tearDown(self):
        pass

    def test_make_public_item(self):
        item = {
            'id': 1,
            'name': 'Apples',
            'amount': 100,
            'unit': 'kpl',
            'price': 10.25,
            'currency': '€',
            'add_time': '2017-04-23T16:15:58Z',
            'add_person': 'test',
            'mod_time': '2017-04-23T16:15:58Z',
            'mod_person': 'test'
        }
        n_item = self.make_public_item(item)
        expected_item = {
            'id': 1,
            'name': 'Apples',
            'amount': 100,
            'unit': 'kpl',
            'price': 10.25,
            'currency': '€',
            'url': '/api/v1.0/catalog/1',
        }
        assert n_item == expected_item

    def test_make_public_basket_item(self):
        item = {
            'user_id': 'cookie',
            'product_id': 1,
            'amount': 20,
            'add_time': time.strftime("%G-%m-%dT%TZ"),
            'mod_time': time.strftime("%G-%m-%dT%TZ")
        }
        n_item = self.make_public_basket_item(item)
        expected_item = {
          "amount": 20,
          "product_id": 1,
          "uri": "/api/v1.0/basket/cookie/1",
          "user_id": "cookie"
        }
        assert n_item == expected_item

    def test_get_amount_of_already_reserved(self):
        test_list = [
            {
                'user_id': 'testman',
                'product_id': 5,
                'amount': 120,
                'add_time': time.strftime("%G-%m-%dT%TZ"),
                'mod_time': time.strftime("%G-%m-%dT%TZ")
            },
            {
                'user_id': 'testman2',
                'product_id': 5,
                'amount': 90,
                'add_time': time.strftime("%G-%m-%dT%TZ"),
                'mod_time': time.strftime("%G-%m-%dT%TZ")
            }
        ]
        r = app.get_amount_of_already_reserved(5, test_list)
        assert r == 210

'''
#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User(nickname='john', email='john@example.com')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
        assert avatar[0:len(expected)] == expected

    def test_make_unique_nickname(self):
        u = User(nickname='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('john')
        assert nickname != 'john'
        u = User(nickname=nickname, email='susan@example.com')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname('john')
        assert nickname2 != 'john'
        assert nickname2 != nickname
'''
if __name__ == '__main__':
    unittest.main()
