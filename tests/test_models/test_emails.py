import pytz
from datetime import datetime, timedelta

from cores import (utils)
# ------------------------------ ORM models
from models.emails import (Email as EmailORM, EmailStatusChoices, EmailQuery)
from models.user_recipients import (UserRecipient, UserRecipientQuery)
from models.email_histories import (EmailHistory, EmailHistoryQuery, EmailHistoryStatusChoices)

from .parents import (ParentTestCase)

# -----------------------------------------------------PREPARE DATA FOR TESTCASE
EMAIL = 'EMAIL_TEST@gmail.com'
EMAIL_SUBJECT = 'EMAIL_SUBJECT_TEST'

# ----------------------------------------------------------------------------------
# -------------------------------------------------------test scenario for manage financial data
class TestModelForFinancial(ParentTestCase):
    """
        Scenario Test
        - [+] manage routing
        -----
        Note:
        1. [+] for positive test || [-] for negative test || [...]P for common test function and written in parent
        2. ...
    """

    @classmethod
    def setUpClass(cls):
        """ call once a time, before setUp and test_* """
        super(TestModelForFinancial, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """ call once a time, after setUp and test_*  """
        super(TestModelForFinancial, cls).tearDownClass()

    def setUp(self):
        ''' auto called before current test_* is calling '''

        self.db.session.rollback()

    def tearDown(self):
        ''' auto called after current test_* is calling '''
        pass

    # -----------------------------------------------------------------------------
    # -------------------------------------------------------------FUNCTION HELPER
    # -------------------------------------------------------------
    def _set_dummy_email(self, event_id: str) -> EmailORM:
        """ create dummy data for email
        :event_id -> event_id input data (unique)
        """

        email_orm = EmailQuery.get_one_filter_by_event_id(event_id=event_id)
        # check data, if not exist yet
        if email_orm is None:
            tz_singapore = utils.get_timezone(timezone="Asia/Singapore")
            dt_input = datetime.strptime('30 Apr 2022 23:12', '%d %b %Y %H:%M')
            dt_normalize = (dt_input - timedelta(hours=8)).replace(tzinfo=pytz.UTC)

            payload = dict(
                event_id=event_id,
                email_subject=self._generate_random_string(15),
                email_content=self._generate_random_string(50),
                timestamp=dt_normalize,

                status=EmailStatusChoices.OPEN
            )

            email_orm = EmailORM(**payload)
            email_orm.save()

            # validate timestamp saved
            dt_loaded = utils.convert_datetime_to_specific_timezone(datetime=email_orm.timestamp, timezone=tz_singapore)
            dt_now = datetime.now(tz=tz_singapore)

            self.assertGreater(dt_loaded, dt_now)

            # validate data db
            del payload['timestamp']
            self._loopAssertEqualForDB(email_orm, payload)

        # validate orm
        self.assertIsNotNone(email_orm.id)

        return email_orm

    def _set_dummy_user_recipient(self, email: str) -> UserRecipient:
        """ create dummy data for user_recipient
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

    def _set_dummy_email_history(self, email_orm: EmailORM, recipient_orm: UserRecipient) -> EmailHistory:
        """ create dummy data for email_history
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

    # -------------------------------------------------------------
    # -------------------------------------------------------------FUNCTION CONSUME
    def test_manage_notif_email(self):
        # prepare data
        email_orm_1 = self._set_dummy_email(event_id=999999)
        email_orm_2 = self._set_dummy_email(event_id=999998)

        recipient_orm = self._set_dummy_user_recipient(email=EMAIL)

        email_history_orm_1 = self._set_dummy_email_history(email_orm=email_orm_1, recipient_orm=recipient_orm)
        email_history_orm_2 = self._set_dummy_email_history(email_orm=email_orm_2, recipient_orm=recipient_orm)

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
