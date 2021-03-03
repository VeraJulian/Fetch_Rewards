import unittest
import json

from tornado.escape import json_encode
from tornado.testing import AsyncHTTPTestCase
from unittest.mock import MagicMock
from unittest.mock import patch

from fetch_rewards_api import Application

"""
Test for example expected results
"""

class TestAPI(AsyncHTTPTestCase):
    def get_app(self):
        return Application()

            
    def test_api(self):
        response = self.fetch('/api/add_transactions', method='POST', body=json.dumps({'payer': 'DANNON', 'points': 1000, 'timestamp': '2020-11-02T14:00:00Z'}))
        self.fetch('/api/add_transactions', method='POST', body=json.dumps({ "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" }))
        self.fetch('/api/add_transactions', method='POST', body=json.dumps({ "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" }))
        self.fetch('/api/add_transactions', method='POST', body=json.dumps({ "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" }))
        self.fetch('/api/add_transactions', method='POST', body=json.dumps({ "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }))
        self.assertEqual(response.body, b'Transaction posted')
        self.assertEqual(response.code, 200)


    def test_spend_points(self):
        response = self.fetch('/api/spend_points', method='POST', body=json.dumps({"points": 5000}))
        self.assertEqual(response.body, b'[{"payer": "DANNON", "points": -100}, {"payer": "UNILEVER", "points": -200}, {"payer": "MILLER COORS", "points": -4700}]')

        
    def test_get_balances(self):
        response = self.fetch('/api/get_balances', method='GET')
        self.assertEqual(response.body, b'{"DANNON": 1000, "UNILEVER": 0, "MILLER COORS": 5300}')
        


if __name__ == '__main__':
    unittest.main()
