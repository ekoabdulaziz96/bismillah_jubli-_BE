import enum
from cores.databases import (Column, PkModelWithManageAttr, db, generate_id, reference_col)

MAX_HISTORY_ID = 32


class EmailHistoryStatusChoices(enum.Enum):
    """Email History for status choices for enum data"""

    OPEN = "OPEN"
    PROCESS = "PROCESS"
    SUCCCESS = "SUCCCESS"
    FAIL = "FAIL"
    PENDING = "PENDING"
    SCHEDULED = "SCHEDULED"

class EmailHistory(PkModelWithManageAttr):
    """ORM class for Email History table"""

    __tablename__ = "email_histories"

    history_id = Column(db.String(MAX_HISTORY_ID), unique=True, nullable=False, default=generate_id)
    status = Column('status', db.Enum(EmailHistoryStatusChoices, name="email_history_status_choices_enum"))

    # many to one relations
    email_id = reference_col("emails", nullable=False)
    user_recipient_id = reference_col("user_recipients", nullable=False)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"EMAIL_HISTORY [{self.history_id}]"


class EmailHistoryQuery(object):
    """ Resource class for doing query data in Email Histories table """

    @classmethod
    def get_one_filter_by_history_id(cls, history_id: str) -> EmailHistory:
        """read data filter by `history_id`
        :history_id -> history_id value for filter data
        """
        return EmailHistory.query.filter_by(history_id=history_id).first()

    @classmethod
    def get_one_filter_by_emailID_and_userRecipientID(cls, email_id: str, user_recipient_id: str) -> EmailHistory:
        """read data filter by `email_id` and `user_recipient_id`
        :email_id -> email_id value for filter data
        :user_recipient_id -> user_recipient_id value for filter data
        """
        return EmailHistory.query.filter_by(email_id=email_id).filter_by(user_recipient_id=user_recipient_id).first()
