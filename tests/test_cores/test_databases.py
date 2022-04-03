import unittest

import server
from cores.extensions import db

# ---------------------------------------------------------------------------------------------------
# --------------------------------------------------------------- Test Connection to NoSQL Databases
class TestDatabaseSqlConnection(unittest.TestCase):
    """ == Class Test for core Databse connection == \n

        Scenario Test
        - [+] test success connection
        -----
        Note: [+] for positive test || [-] for negative test || [...]P for common test function and written in parent
    """
    @classmethod
    def setUpClass(cls):
        """ call once a time """
        super(TestDatabaseSqlConnection, cls).setUpClass()
        # instance app Flask and client
        cls.app = server.app
        cls.app.debug = True
        cls.client = cls.app.test_client()

    def test_success_connection(self):
        conn_status = False
        try:
            db.app = self.app
            if db.session.execute('SELECT 1'):
                conn_status = True
        except Exception as e:       # pragma: no cover
            print('sql db not connect', e)

        self.assertTrue(conn_status)
