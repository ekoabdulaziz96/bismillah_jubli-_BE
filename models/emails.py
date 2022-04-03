
import enum
from typing import List
from datetime import datetime, timedelta

from cores import (utils, constants as const)
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

    __table_args__ = (
        # Constrain Indexes
        db.Index(
            'email_idx_for_need_to_process',                         # Index name
            status, timestamp.asc()    # Columns which are part of the index
        ),
    )

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"EMAIL [{self.event_id}] {self.email_subject[:25]}..."


class EmailQuery(object):
    """ Resource class for doing query data in Emails table """

    @classmethod
    def get_one_filter_by_event_id(cls, event_id: str) -> Email:
        """read one data filter by `event_id`
        :event_id -> event_id value for filter data
        """
        return Email.query.filter_by(event_id=event_id).first()

    @classmethod
    def get_all_filter_by_email_subject(cls, email_subject: str) -> List[Email]:
        """read all data filter by `email_subject`
        :email_subject -> email_subject value for filter data
        """
        return Email.query.filter_by(email_subject=email_subject).all()

    @classmethod
    def get_all_filter_by_current_datetime_tz_singapore(cls) -> List[Email]:
        """read all data filter by `datetime_now`
        :datetime_now -> datetime_now value for filter data
        """
        tz_singapore = utils.get_timezone('Asia/Singapore')
        dt_now_str = (datetime.now(tz=tz_singapore) - timedelta(hours=8)).strftime(const.ConstEmail.FORMAT_TIMESTAMP)
        dt_now = datetime.strptime(dt_now_str, const.ConstEmail.FORMAT_TIMESTAMP)

        return Email.query.filter_by(timestamp=dt_now).filter_by(status=EmailStatusChoices.OPEN).all()
