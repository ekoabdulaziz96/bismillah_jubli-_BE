import random
import unittest
from datetime import datetime, timedelta

from cores import (constants as const)
from models import (emails as mdlEmails)
from schemas import (emails as schEmails)
from .parents import (ParentTestSchema)

# ------------------------------------------------------------------
# -------------------------------------------------STATIC DATA
random_str = ParentTestSchema.getRandomString(15)

# ------------------------------------------EMAIL
EMAIL_PAYLOAD_MANDATORY = dict(
    event_id=random.randint(49999, 99999),
    email_subject=random_str,
    email_content=random_str,
    timestamp=(datetime.now() + timedelta(hours=2)).strftime(const.ConstEmail.FORMAT_TIMESTAMP)
)

# ----------------------------------------------------------------------
# ---------------------------------------------------TEST SCHEMA FOR FINANCIAL SERVICE
class TestEmailRequestSchema(unittest.TestCase, ParentTestSchema):
    """ == Class Test Email Create/Update for payload data in request body == \n
        Scenario Test
        #### from parent test
        - [+]P test payload with all field (include optional field)
        - [+]P test payload with only mandatory field
        - [-]P test payload without data
        - [-]P test payload with unregistered key

        #### origin test case
        - [-] test payload with invalid negative value of event_id
        - [-] test payload with invalid max length of email_subject
        - [-] test payload with invalid timestamp cz not sended
        - [-] test payload with invalid timestamp format
        - [-] test payload with invalid timestamp value

        -----
        Note: [+] for positive test || [-] for negative test || [...]P for common test function and written in parent
    """

    def setUp(self):
        ''' auto called before current test_* is calling '''

        # prepare data to consume all of test function
        self.payload_mandatory_only = EMAIL_PAYLOAD_MANDATORY.copy()
        self.payload_full = EMAIL_PAYLOAD_MANDATORY.copy()

        self.schema = schEmails.EmailSchema()

    # -------------------------------------------------------------
    # --------------------------------------------function helper
    # -
    # -------------------------------------------------------------
    # --------------------------------------------function consume
    # override test
    def test_payload_with_all_field(self):
        valid_data = self.schema.load(self.payload_full)

        # check count valid data
        self.assertEqual(len(valid_data), len(self.payload_full))
        # check key in valid data
        self._loopAssertInForKeys(loopKeyData=valid_data, expectData=self.payload_full)

        # check value in valid data
        self.assertEqual(type(valid_data['timestamp']), datetime)
        del valid_data['timestamp']
        self._loopAssertEqual(currData=valid_data, expectData=self.payload_full)

    # override test
    def test_payload_with_only_mandatory_field(self):
        valid_data = self.schema.load(self.payload_mandatory_only)

        # check count valid data
        self.assertEqual(len(valid_data), len(self.payload_mandatory_only))
        # check key in valid data
        self._loopAssertInForKeys(loopKeyData=valid_data, expectData=self.payload_mandatory_only)

        # check value in valid data
        self.assertEqual(type(valid_data['timestamp']), datetime)
        del valid_data['timestamp']
        self._loopAssertEqual(currData=valid_data, expectData=self.payload_mandatory_only)

    def test_payload_with_invalid_negative_value_of_event_id(self):
        # prepare invalid data
        key = 'event_id'
        payload_invalid = self.payload_full.copy()
        payload_invalid[key] = -1

        self._invalidValidatePayload(payload_invalid, key=key, err_message=schEmails.MESSAGE_POSITIVE_MIN_ONE)

    def test_payload_with_invalid_max_length_of_email_subject(self):
        key = 'email_subject'
        self._invalidMaxLengthPayload(key=key, maxLength=mdlEmails.MAX_EMAIL_SUBJECT)

    def test_payload_with_invalid_timestamp_cz_not_sended(self):
        # prepare invalid data
        key = 'timestamp'
        old_value = self.payload_full[key]
        del self.payload_full[key]

        self._invalidValidatePayload(data=self.payload_full, key=key, err_message=self.err_message_missing_required)

        # tear down locally
        self.payload_full[key] = old_value

    def test_payload_with_invalid_timestamp_format(self):
        # prepare invalid data
        key = 'timestamp'
        old_value = self.payload_full[key]
        self.payload_full[key] = self.getRandomString(15)

        self._invalidValidatePayload(data=self.payload_full, key=key, err_message=schEmails.MESSAGE_INVALID_TIMESTAMP_FORMAT)

        # tear down locally
        self.payload_full[key] = old_value

    def test_payload_with_invalid_timestamp_value(self):
        # prepare invalid data
        key = 'timestamp'
        old_value = self.payload_full[key]
        self.payload_full[key] = "15 Dec 2015 23:12"

        self._invalidValidatePayload(data=self.payload_full, key=key, err_message=schEmails.MESSAGE_INVALID_TIMESTAMP_VALUE)

        # tear down locally
        self.payload_full[key] = old_value
