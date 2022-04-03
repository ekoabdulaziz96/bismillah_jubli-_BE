import unittest
import time

import server
from cores.extensions import cache

# ---------------------------------------------------------------------------------------------------
# --------------------------------------------------------------- Test Connection to NoSQL Databases
class TestCacheConnection(unittest.TestCase):
    """ == Class Test for core Memory Chache connection == \n

        Scenario Test
        - [+] test success chache
        -----
        Note: [+] for positive test || [-] for negative test || [...]P for common test function and written in parent
    """

    @classmethod
    def setUpClass(cls):
        """ call once a time """
        super(TestCacheConnection, cls).setUpClass()
        # instance app Flask and client
        cls.app = server.app
        cls.app.debug = True
        cls.client = cls.app.test_client()

    def test_success_cache(self):
        cache.init_app(self.app)

        result = cache.set('name_key', 'custom_value', 1)     # key, valvue, timeout in seconds
        self.assertTrue(result)
        self.assertEqual(cache.get('name_key'), 'custom_value')

        time.sleep(1)
        self.assertNotEqual(cache.get('name_key'), 'custom_value')
