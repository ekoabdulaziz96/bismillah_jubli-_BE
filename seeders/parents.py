import sys
import os
import random
import string
import server
from cores import (databases)

""" set relative path """
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

class ParentSeeder(object):
    """ parent class for seeder """

    def __init__(self):
        """ constructor for seeder, init app and db"""
        self.app = server.app
        self.app.debug = True

        self.db = databases.db
        self.db.app = self.app

    @classmethod
    def _generate_random_string(self, length: int):
        """ return random string with size length :param `length`(int)"""

        random_str = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
        return random_str

    def _seed_table_with_one_filter(self, ORM_class: object, filter_data: dict, payload: dict) -> None:
        """ create dummy data for table, using procedure get or create

        :ORM_class -> ORM class that relate a table in DB
        :filter_data -> filter data for exist or not in DB
        :payload -> payload data to be added
        """
        data_record = ORM_class.query.filter_by(**filter_data).first()

        if not data_record:
            payload = payload

            data_record = ORM_class(**payload)
            data_record.save()
            print(f'|SUCCES ADD NEW DATA|-{data_record}')
        else:
            print(f'|DATA EXIST|-{data_record}')

        return data_record

    def _seed_table_with_two_filter(self, ORM_class: object, filter_data1: dict, filter_data2: dict, payload: dict) -> None:
        """ create dummy data for table, using procedure get or create

        :ORM_class -> ORM class that relate a table in DB
        :filter_data1 -> filter data for exist or not in DB
        :filter_data2 -> filter data for exist or not in DB
          -> using AND logic for filter_data1 AND filter_data2 in where clause
        :payload -> payload data to be added
        """
        data_record = ORM_class.query.filter_by(**filter_data1).filter_by(**filter_data2).first()

        if not data_record:
            payload = payload

            data_record = ORM_class(**payload)
            data_record.save()
            print(f'|SUCCES ADD NEW DATA|-{data_record}')
        else:
            print(f'|DATA EXIST|-{data_record}')
