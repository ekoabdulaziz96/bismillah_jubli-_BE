import requests
from datetime import datetime
from unittest import mock

from cores import (utils, constants as const)
from services.modules.emails import (Email as moduleEmails)
from ..test_models.test_emails import (Helper as HelperTestModelEmail)
# ------------------------------ ORM models
from models.emails import (EmailQuery)
from models.email_histories import (EmailHistoryQuery, EmailHistoryStatusChoices)

from .parents import (ParentTestCase)

# -----------------------------------------------------PREPARE DATA FOR TESTCASE
EMAIL_SUBJECT = 'EMAIL_SUBJECT_TEST'

# ----------------------------------------------------------------------------------
# -------------------------------------------------------helper
class Helper(HelperTestModelEmail):
    """ Helper class for test module send email
    """
    @classmethod
    def _reset_dummy_data_for_scenario_test_modul_send_email(cls):
        """ reset dummy data for scenarion test module send email"""
        email_orm_list = EmailQuery.get_all_filter_by_email_subject(email_subject=EMAIL_SUBJECT)
        for email_orm in email_orm_list:
            for email_history_orm in email_orm.email_histories:
                email_history_orm.delete()

            email_orm.delete()

        cls._reset_dummy_data_email()

# -------------------------------------------------------test scenario for send email
class TestModuleEmailForScenarionSendEmail(ParentTestCase):
    """ == Class Test Module Email for scenarion send email == \n
        Scenario Test
        - [] Test Send Email Fail
        - [+] Test Send Email Success
        -----
        Note:
        1. [+] for positive test || [-] for negative test || [...]P for common test function and written in parent
        2. ...
    """

    @classmethod
    def setUpClass(cls):
        """ call once a time, before setUp and test_* """
        super(TestModuleEmailForScenarionSendEmail, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """ call once a time, after setUp and test_*  """
        super(TestModuleEmailForScenarionSendEmail, cls).tearDownClass()

        # Cleaning email
        Helper._reset_dummy_data_for_scenario_test_modul_send_email()

    def setUp(self):
        ''' auto called before current test_* is calling '''

        self.db.session.rollback()
        self.tz_singapore = utils.get_timezone(timezone="Asia/Singapore")

    def tearDown(self):
        ''' auto called after current test_* is calling '''
        pass

    # -----------------------------------------------------------------------------
    # -------------------------------------------------------------FUNCTION HELPER
    # -
    # -------------------------------------------------------------
    # -------------------------------------------------------------FUNCTION CONSUME
    def test_manage_notif_fail(self):
        # prepare data
        timestamp = (datetime.now(tz=self.tz_singapore)).strftime(const.ConstEmail.FORMAT_TIMESTAMP)
        email_orm_1 = Helper._set_dummy_email(self=self, event_id=-1, timestamp=timestamp)
        email_orm_2 = Helper._set_dummy_email(self=self, event_id=-2, timestamp=timestamp)
        email_orm_list = [email_orm_1, email_orm_2]
        email_id_list = [email_orm_1.id, email_orm_2.id]

        Helper._set_dummy_user_recipient(self=self, email='azizeko29undip@gmail.com')
        Helper._set_dummy_user_recipient(self=self, email='azizeko12undip@gmail.com')

        mock_connection_timeout = requests.exceptions.ConnectTimeout('mock_connection_timeout')
        # with mock.patch("flask_mail.Connection.send.__repr__", return_value='success'):                   # turn off mock
        with mock.patch("flask_mail.Connection.send", side_effect=mock_connection_timeout):                   # turn on mock
            with self.app.app_context():
                moduleEmails().process_send_email(email_orm_list=email_orm_list)

        # new session DB in here
        for email_id in email_id_list:
            email_history_orm_list = EmailHistoryQuery.get_all_filter_by_email_id(email_id=email_id)
            self.assertGreaterEqual(len(email_history_orm_list), 2)
            for email_history_orm in email_history_orm_list:
                self.assertEqual(email_history_orm.status, EmailHistoryStatusChoices.FAIL)

        # tear down locally
        Helper._reset_dummy_data_for_scenario_test_modul_send_email()

    def test_manage_notif_email(self):
        # prepare data
        timestamp = (datetime.now(tz=self.tz_singapore)).strftime(const.ConstEmail.FORMAT_TIMESTAMP)
        email_orm_1 = Helper._set_dummy_email(self=self, event_id=-1, timestamp=timestamp)
        email_orm_2 = Helper._set_dummy_email(self=self, event_id=-2, timestamp=timestamp)
        email_orm_list = [email_orm_1, email_orm_2]
        email_id_list = [email_orm_1.id, email_orm_2.id]

        Helper._set_dummy_user_recipient(self=self, email='azizeko29undip@gmail.com')
        Helper._set_dummy_user_recipient(self=self, email='azizeko12undip@gmail.com')

        # with mock.patch("flask_mail.Connection.send.__repr__", return_value='success'):       # turn off mock
        with mock.patch("flask_mail.Connection.send", return_value='success'):                  # turn on mock
            with self.app.app_context():
                moduleEmails().process_send_email(email_orm_list=email_orm_list)

        # new session DB in here
        for email_id in email_id_list:
            email_history_orm_list = EmailHistoryQuery.get_all_filter_by_email_id(email_id=email_id)
            self.assertGreaterEqual(len(email_history_orm_list), 2)
            for email_history_orm in email_history_orm_list:
                self.assertEqual(email_history_orm.status, EmailHistoryStatusChoices.SUCCCESS)

        # tear down locally
        Helper._reset_dummy_data_for_scenario_test_modul_send_email()
# end class
