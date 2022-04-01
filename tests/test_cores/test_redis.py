import unittest
import time

import server
from cores.extensions import cache

# ---------------------------------------------------------------------------------------------------
# --------------------------------------------------------------- Test Connection to NoSQL Databases
class TestRedisConnection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ call once a time """
        super(TestRedisConnection, cls).setUpClass()
        # instance app Flask and client
        cls.app = server.app
        cls.app.debug = True
        cls.client = cls.app.test_client()

    def test_cache(self):
        cache.init_app(self.app)

        result = cache.set('name_key', 'custom_value', 1)     # key, valvue, timeout in seconds
        self.assertTrue(result)
        self.assertEqual(cache.get('name_key'), 'custom_value')

        time.sleep(1)
        self.assertNotEqual(cache.get('name_key'), 'custom_value')
