import pytz
from datetime import datetime, timedelta

from cores import (utils, constants as const)
# ------------------------------ ORM models
from models.emails import (Email as EmailORM, EmailStatusChoices, EmailQuery)
from models.user_recipients import (UserRecipient, UserRecipientQuery)
from models.email_histories import (EmailHistory, EmailHistoryQuery, EmailHistoryStatusChoices)

from .parents import (ParentTestCase)

# -----------------------------------------------------PREPARE DATA FOR TESTCASE
EMAIL = 'EMAIL_TEST@gmail.com'
EMAIL_SUBJECT = 'EMAIL_SUBJECT_TEST'

# ----------------------------------------------------------------------------------
# -------------------------------------------------------helper
class Helper:
    """ Helper class for manage send email
    """
    @classmethod
    def _set_dummy_email(cls, self: object, event_id: str, timestamp: str = '30 Apr 2022 23:12') -> EmailORM:
        """ create dummy data for email
        :self -> unittest obj
        :event_id -> event_id input data (unique)
        :timestamp -> timestamp input data
        """

        email_orm = EmailQuery.get_one_filter_by_event_id(event_id=event_id)
        # check data, if not exist yet
        if email_orm is None:
            dt_input = datetime.strptime(timestamp, const.ConstEmail.FORMAT_TIMESTAMP)
            dt_normalize = (dt_input - timedelta(hours=8)).replace(tzinfo=pytz.UTC)

            payload = dict(
                event_id=event_id,
                email_subject=EMAIL_SUBJECT,
                email_content=self._generate_random_string(50),
                timestamp=dt_normalize,

                status=EmailStatusChoices.OPEN
            )

            email_orm = EmailORM(**payload)
            email_orm.save()

            # validate timestamp saved
            dt_loaded = utils.convert_datetime_to_specific_timezone(datetime=email_orm.timestamp, timezone=self.tz_singapore) + timedelta(minutes=1)
            dt_now = datetime.now(tz=self.tz_singapore)
            self.assertGreaterEqual(dt_loaded, dt_now)

            # validate data db
            del payload['timestamp']
            self._loopAssertEqualForDB(email_orm, payload)

        # validate orm
        self.assertIsNotNone(email_orm.id)

        return email_orm

    @classmethod
    def _set_dummy_user_recipient(cls, self: object, email: str) -> UserRecipient:
        """ create dummy data for user_recipient
        :self -> unittest obj
        :email -> email input data (unique)
        """

        recipient_orm = UserRecipientQuery.get_one_filter_by_email(email=email)
        # check data, if not exist yet
        if recipient_orm is None:
            payload = dict(
                email=email,
            )

            recipient_orm = UserRecipient(**payload)
            recipient_orm.save()

            # validate data db
            self._loopAssertEqualForDB(recipient_orm, payload)

        # validate orm
        self.assertIsNotNone(recipient_orm.id)

        return recipient_orm

    @classmethod
    def _set_dummy_email_history(cls, self: object, email_orm: EmailORM, recipient_orm: UserRecipient) -> EmailHistory:
        """ create dummy data for email_history
        :self -> unittest obj
        :email_orm -> ORM for email
        :recipient_orm -> ORM for user_recipient
        """

        email_history_orm = EmailHistoryQuery.get_one_filter_by_emailID_and_userRecipientID(email_id=email_orm.id, user_recipient_id=recipient_orm.id)

        # check data if not exist yet
        if email_history_orm is None:
            payload = dict(
                email=email_orm,
                user_recipient=recipient_orm,

                status=EmailHistoryStatusChoices.OPEN,
            )
            email_history_orm = EmailHistory(**payload)
            email_history_orm.save()

            # validate data db
            self._loopAssertEqualForDB(email_history_orm, payload)

        # validate orm
        self.assertIsNotNone(email_history_orm.id)

        return email_history_orm

    @classmethod
    def _reset_dummy_data_email(cls):
        email_orm_list = EmailQuery.get_all_filter_by_email_subject(email_subject=EMAIL_SUBJECT)
        if len(email_orm_list) > 0:
            for email_orm in email_orm_list:
                email_orm.delete()

# -------------------------------------------------------test scenario for send email
class TestModelForScenarionSendEmail(ParentTestCase):
    """ == Class Test Model (ORM) for scenarion send email == \n
        Scenario Test
        - [+] email query function for filter by current datetime with tz singapore
        - [+] manage notif email
        -----
        Note:
        1. [+] for positive test || [-] for negative test || [...]P for common test function and written in parent
        2. ...
    """

    @classmethod
    def setUpClass(cls):
        """ call once a time, before setUp and test_* """
        super(TestModelForScenarionSendEmail, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """ call once a time, after setUp and test_*  """
        super(TestModelForScenarionSendEmail, cls).tearDownClass()

        # Cleaning email
        Helper._reset_dummy_data_email()

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
    def test_email_query_function_for_filter_by_current_datetime_with_tz_singapore(self):
        # prepare data
        timestamp = (datetime.now(tz=self.tz_singapore)).strftime(const.ConstEmail.FORMAT_TIMESTAMP)
        timestamp_plus = (datetime.now(tz=self.tz_singapore) + timedelta(hours=1)).strftime(const.ConstEmail.FORMAT_TIMESTAMP)
        email_orm_1 = Helper._set_dummy_email(self=self, event_id=-1, timestamp=timestamp)
        email_orm_2 = Helper._set_dummy_email(self=self, event_id=-2, timestamp=timestamp)
        email_orm_3 = Helper._set_dummy_email(self=self, event_id=-3, timestamp=timestamp_plus)

        email_orm_list = EmailQuery.get_all_filter_by_current_datetime_tz_singapore()
        self.assertIsNotNone(email_orm_list)
        self.assertEqual(len(email_orm_list), 2)
        self.assertEqual(email_orm_1, email_orm_list[0])
        self.assertEqual(email_orm_2, email_orm_list[1])

        # TEAR_DOWN_LOCALLY
        email_orm_1.delete()
        email_orm_2.delete()
        email_orm_3.delete()

    def test_manage_notif_email(self):
        # prepare data
        email_orm_1 = Helper._set_dummy_email(self=self, event_id=-4)
        email_orm_2 = Helper._set_dummy_email(self=self, event_id=-5)

        recipient_orm = Helper._set_dummy_user_recipient(self=self, email=EMAIL)

        email_history_orm_1 = Helper._set_dummy_email_history(self=self, email_orm=email_orm_1, recipient_orm=recipient_orm)
        email_history_orm_2 = Helper._set_dummy_email_history(self=self, email_orm=email_orm_2, recipient_orm=recipient_orm)

        # cek print (method __repr__)
        print(email_orm_1)
        print(email_orm_2)
        print(recipient_orm)
        print(email_history_orm_1)
        print(email_history_orm_2)

        # TEAR_DOWN_LOCALLY
        email_history_orm_1.delete()
        email_history_orm_2.delete()

        recipient_orm.delete()

        email_orm_1.delete()
        email_orm_2.delete()

# end class
