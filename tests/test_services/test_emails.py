import random
from datetime import datetime

from cores import (constants as const)
from schemas import (emails as schEmails)
from models.emails import (EmailQuery)
from .parents import (ParentPostTestService, ParentTestCase)
from ..test_schemas import (test_emails as testSchEmails)

# -----------------------------------------------------PREPARE DATA FOR TESTCASE
HEADERS_DEFAULT = {'Content-Type': "application/json"}
EMAIL_SUBJECT_TEST = 'EMAIL_SUBJECT_TEST'

# ---------------------------------------------------------------------------------- class parent/helper
class Helper(object):
    """"Helper test in email"""

    @classmethod
    def reset_dummy_data_in_email(cls):
        """clear all dummy data email in DB
        """
        email_list = EmailQuery.get_all_filter_by_email_subject(email_subject=EMAIL_SUBJECT_TEST)
        for email_orm in email_list:
            email_orm.delete()

    @classmethod
    def validate_response_message_data_type(cls, self: object, message_data: dict):
        """ validate response message_data type
        :self -> obj unittest
        :message_data -> message_data in reponse
        """
        # validate message data for value type
        self.assertIsInstance(message_data.get('email_id'), str)
        self.assertIsInstance(message_data.get('event_id'), int)
        self.assertIsInstance(message_data.get('email_subject'), str)
        self.assertIsInstance(message_data.get('email_content'), str)

        self.assertIsInstance(message_data.get('timestamp'), str)
        self.assertIsInstance(datetime.strptime(message_data.get('timestamp'), const.ConstEmail.FORMAT_TIMESTAMP), datetime)
        self.assertIsInstance(message_data.get('status'), str)

    @classmethod
    def validate_response_message_data(cls, self: object, message_data: dict, payload: dict):
        """ validate response message_data value and type
        :self -> obj unittest
        :message_data -> message_data in reponse
        :payload -> payload input data
        :is_active -> is_active bank data
        """
        # validate message data for value type
        cls.validate_response_message_data_type(self=self, message_data=message_data)

        # validate message data for value
        self.assertNotEqual(message_data.get('email_id'), None)
        self.assertEqual(message_data.get('event_id'), payload.get('event_id'))
        self.assertEqual(message_data.get('email_subject'), payload.get('email_subject'))
        self.assertEqual(message_data.get('email_content'), payload.get('email_content'))

        self.assertEqual(message_data.get('timestamp'), payload.get('timestamp'))
        self.assertNotEqual(message_data.get('status'), None)

# end class

# -------------------------------------------------------test bank create
class TestEmailSave(ParentTestCase, ParentPostTestService):
    """== Class integration test for endpoint save_emails == \n
        Scenario Test
        #### from helper parent post test
        - [-]P Content-Type in header is not sended
        - [-]P Content-Type in header is not correct for json syntax  ("application/json")
            - for child test , content-type json is corrent

        #### origin test case
        - [-] invalid schema payload for timestamp format
        - [-] invalid schema payload for timestamp value
        - [+] success save email
        - [-] fail save email cz event_id already exist
        -----
        Note:
        1. [+] for positive test || [-] for negative test || [...]P for common test function and written in parent
        2. bl -> business logic
    """

    @classmethod
    def setUpClass(cls):
        """ call once a time, before setUp and test_* """
        super(TestEmailSave, cls).setUpClass()
        # -- prepare attr for class parent ParentTestServices
        cls.req_method = 'POST'
        cls.email_subject = EMAIL_SUBJECT_TEST

    @classmethod
    def tearDownClass(cls):
        """ call once a time, after setUp and test_*  """
        super(TestEmailSave, cls).tearDownClass()
        # reset dummy data
        Helper.reset_dummy_data_in_email()

    def setUp(self):
        ''' auto called before current test_* is calling '''

        # prepare data to consume all of test function
        # -- prepare attr for class parent ParentTestServices
        self.url = const.ConstRouteEmail.SAVE_EMAIL
        # prepare headers
        self.headers = HEADERS_DEFAULT.copy()
        # prepare payload
        self.payload = testSchEmails.EMAIL_PAYLOAD_MANDATORY.copy()
        self.payload['event_id'] = random.randint(49999, 99999)
        self.payload['email_subject'] = self.email_subject

        self.init_serialize = list(schEmails.EmailSchemaSerializer.Meta.fields)

    def tearDown(self):
        ''' auto called after current test_* is calling '''
        pass

    # -----------------------------------------------------------------------------
    # -------------------------------------------------------------FUNCTION HELPER
    # -
    # -----------------------------------------------------------------------------
    # -------------------------------------------------------------FUNCTION CONSUME
    def test_invalid_schema_payload_for_timestamp_format(self):
        # prepare data
        key = 'timestamp'
        old_value = self.payload[key]
        self.payload[key] = "15 December 2015 23:12"

        # do request
        response = self._doTestAndValidateExceptMessageData(test='error', message_code='INVALID_REQUEST_PARAMETER')

        # validate message data
        message_data = response.get('message_data')
        self.assertNotEqual(message_data, {})
        # validate value message data
        for errData in message_data:
            self.assertIn(key, errData.values())
            self.assertEqual(errData.get('description'), schEmails.MESSAGE_INVALID_TIMESTAMP_FORMAT)

        # TEAR_DOWN_LOCAL
        self.payload[key] = old_value

    def test_invalid_schema_payload_for_timestamp_value(self):
        # prepare data
        key = 'timestamp'
        old_value = self.payload[key]
        self.payload[key] = "15 Dec 2015 23:12"

        # do request
        response = self._doTestAndValidateExceptMessageData(test='error', message_code='INVALID_REQUEST_PARAMETER')

        # validate message data
        message_data = response.get('message_data')
        self.assertNotEqual(message_data, {})
        # validate value message data
        for errData in message_data:
            self.assertIn(key, errData.values())
            self.assertEqual(errData.get('description'), schEmails.MESSAGE_INVALID_TIMESTAMP_VALUE)

        # TEAR_DOWN_LOCAL
        self.payload[key] = old_value

    def _test_success_save_email(self):

        # do request
        response_json = self._doTestAndValidateExceptMessageData(test='success', message_code='SUCCESS_CREATE')
        message_data = response_json.get('message_data')

        # validate message data for key
        self._assertInForKeys(loopKeyData=message_data, expectData=self.init_serialize)
        self.assertNotEqual(message_data, {})

        # validate message data for value
        Helper.validate_response_message_data(self=self, message_data=message_data, payload=self.payload)

    def test_fail_save_email_cz_event_id_already_exist(self):
        # create new bank
        self._test_success_save_email()

        # create new bank again with same data
        self._doFailTestAndValidate(err_message_code='EVENT_ID_ALREADY_EXIST')

    # ---------------------------------------------------------------------------------------------
    # not tested, only for eksplore or debug
    def _test_mock_eksplore(self):   # pragma: no cover
        pass
# end class
