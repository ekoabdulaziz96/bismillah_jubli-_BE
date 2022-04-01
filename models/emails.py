
import enum
from typing import List
from cores.databases import (Column, PkModelWithManageAttr, db, relationship, generate_id)

MAX_EMAIL_SUBJECT = 100
MAX_EMAIL_ID = 32

class EmailStatusChoices(enum.Enum):
    """Email for status choices for enum data"""

    OPEN = "OPEN"
    SCHEDULED = "SCHEDULED"
    PROCESSED = "PROCESSED"

class Email(PkModelWithManageAttr):
    """ORM class for Email table"""

    __tablename__ = "emails"

    email_id = Column(db.String(MAX_EMAIL_ID), unique=True, nullable=False, default=generate_id)

    event_id = Column(db.Integer, nullable=False, unique=True)
    email_subject = Column(db.String(MAX_EMAIL_SUBJECT), nullable=False)
    email_content = Column(db.Text, nullable=False)
    timestamp = Column(db.DateTime(timezone=True), nullable=False)

    status = Column('status', db.Enum(EmailStatusChoices, name="email_status_choices_enum"))

    # one to many relations
    email_histories = relationship("EmailHistory", backref="email", lazy="dynamic")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"EMAIL [{self.event_id}] {self.email_subject[:25]}..."


class EmailQuery(object):
    """ Resource class for doing query data in Emails table """

    @classmethod
    def get_one_filter_by_event_id(cls, event_id: str) -> Email:
        """read data filter by `event_id`
        :event_id -> event_id value for filter data
        """
        return Email.query.filter_by(event_id=event_id).first()

    @classmethod
    def get_filter_by_email_subject(cls, email_subject: str) -> List[Email]:
        """read data filter by `email_subject`
        :email_subject -> email_subject value for filter data
        """
        return Email.query.filter_by(email_subject=email_subject).all()
