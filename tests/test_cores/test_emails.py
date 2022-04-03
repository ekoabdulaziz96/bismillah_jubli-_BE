import unittest

import server
from cores.extensions import mail

# ---------------------------------------------------------------------------------------------------
# --------------------------------------------------------------- Test Connection to NoSQL Databases
class TestMailConnection(unittest.TestCase):
    """ == Class Test for core Mail connection == \n

        Scenario Test
        - [+] test success mail
        -----
        Note: [+] for positive test || [-] for negative test || [...]P for common test function and written in parent
    """

    @classmethod
    def setUpClass(cls):
        """ call once a time """
        super(TestMailConnection, cls).setUpClass()
        # instance app Flask and client
        cls.app = server.app
        cls.app.debug = True
        cls.client = cls.app.test_client()

    def test_success_mail(self):
        #  https://pythonhosted.org/Flask-Mail/#unit-tests-and-suppressing-emails
        with mail.record_messages() as outbox:
            with self.app.app_context():
                mail.send_message(
                    subject='testing',
                    body='test',
                    recipients=['azizeko29undip@gmail.com']
                )

            assert len(outbox) == 1
            assert outbox[0].subject == "testing"
