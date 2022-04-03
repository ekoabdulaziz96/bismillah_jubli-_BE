import random
import string
from unittest import (TestCase)

import server
from cores import (databases)


# create your own parent unittest here or inherit then put your own version 1,2,3
# ex : ParentTestServicesV2
# -------------------------------------------------------------
# -------------------------------------------------------PARENT TEST CASE
class ParentTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        """ call once a time """
        super(ParentTestCase, cls).setUpClass()
        # instance app Flask and client
        cls.app = server.app
        cls.app.debug = True
        cls.client = cls.app.test_client()

        # instance db sqlalchemy
        cls.db = databases.db
        cls.db.app = cls.app

    # -----------------------------------------------------------------------------
    # -------------------------------------------------------------FUNCTION HELPER
    def _generate_random_string(self, length: int):
        """ generate random string that have length as input

        :length -> length of generated random string
        """
        random_str = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
        return random_str

    def _loopAssertEqualForDB(self, ORM_object: object, payload: dict):
        """ loop assert equal, for test payload data is saved in db

        :ORM_object -> instance object from specific ORM class
        :payload -> input payload data
        """
        for key in payload.keys():
            self.assertEqual(getattr(ORM_object, key), payload.get(key))

# end class
