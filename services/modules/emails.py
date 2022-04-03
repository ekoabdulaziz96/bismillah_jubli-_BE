from typing import List
from flask_mail import Message

from cores.extensions import (mail)
from models.emails import (Email as mdlEmail, EmailStatusChoices)
from models.user_recipients import (UserRecipientQuery)
from models.email_histories import (EmailHistory, EmailHistoryStatusChoices, MAX_MESSAGE)


class Email:
    """ class module for email
    """
    # ------------------------------------------------ Helper Function
    # ------------------------------------------------ Helper Function
    def _send_email(self, email_orm: mdlEmail):
        """ function for send email
        :email_orm -> ORM for email
        """
        users = UserRecipientQuery.get_all_of_active_recipient()
        subject = email_orm.email_subject
        message = email_orm.email_content
        with mail.connect() as conn:
            for user in users:
                email_history_orm = EmailHistory(email=email_orm, user_recipient=user, status=EmailHistoryStatusChoices.PROCESS)
                email_history_orm.save()
                try:
                    msg = Message(recipients=[user.email], body=message, subject=subject)
                    conn.send(msg)

                    email_history_orm.update(status=EmailHistoryStatusChoices.SUCCCESS)
                except Exception as e:
                    email_history_orm.update(status=EmailHistoryStatusChoices.FAIL, message=str(e)[:MAX_MESSAGE])

    # ------------------------------------------------ Consume Function
    def process_send_email(self, email_orm_list: List[mdlEmail]):
        """ function for process send email
        :email_orm_list -> list of ORM email
        """
        for email_orm in email_orm_list:
            email_orm.update(status=EmailStatusChoices.PROCESSED)
            self._send_email(email_orm)
