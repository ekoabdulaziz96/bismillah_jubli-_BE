import sys
import os
# from datetime import datetime, timedelta

""" set relative path """
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

# ------------------------------ ORM models
from models.user_recipients import (UserRecipient)
from seeders.parents import (ParentSeeder)

# ----------------------------------------------------- PREPARE SEED DATA
PAYLOAD_USER_RECIPIENT_LIST = [
    dict(
        email='azizeko29undip@gmail.com',
    ),
    dict(
        email='azizeko12undip@gmail.com',
    ),
]

# ----------------------------------------------------- CLASS SEEDER
class SeedUserRecipient(ParentSeeder):
    """ class for make a seed data for User Recipient"""

    def process(self):
        """process seeder transfer-on-us"""
        try:
            # seed data for table notif variable
            for payload in PAYLOAD_USER_RECIPIENT_LIST:
                filter_data = dict(email=payload.get('email'))
                self._seed_table_with_one_filter(UserRecipient, filter_data, payload)

        except Exception as e:
            print(f'|ERROR|-{e}')


# -------------------------------------------------------run script
if __name__ == '__main__':
    SeedUserRecipient().process()
