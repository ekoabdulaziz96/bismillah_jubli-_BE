from typing import List
from cores.databases import (Column, PkModelWithManageAttr, db, relationship, generate_id)

MAX_RECIPIENT_ID = 32
MAX_EMAIL = 50


class UserRecipient(PkModelWithManageAttr):
    """ORM class for User Recipient table"""

    __tablename__ = "user_recipients"

    recipient_id = Column(db.String(MAX_RECIPIENT_ID), unique=True, nullable=False, default=generate_id)
    email = Column(db.String(MAX_EMAIL), nullable=False, unique=True)

    # one to many relations
    email_histories = relationship("EmailHistory", backref="user_recipient", lazy="dynamic")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"USER_RECIPIENT [{self.recipient_id}] {self.email}"


class UserRecipientQuery(object):
    """ Resource class for doing query data in Emails table """

    @classmethod
    def get_one_filter_by_recipient_id(cls, recipient_id: str) -> UserRecipient:
        """read one data filter by `recipient_id`
        :recipient_id -> recipient_id value for filter data
        """
        return UserRecipient.query.filter_by(recipient_id=recipient_id).first()

    @classmethod
    def get_one_filter_by_email(cls, email: str) -> UserRecipient:
        """read one data filter by `email`
        :email -> email value for filter data
        """
        return UserRecipient.query.filter_by(email=email).first()

    @classmethod
    def get_all_of_active_recipient(cls) -> List[UserRecipient]:
        """get all of active recipient
        :email -> email value for filter data
        """
        return UserRecipient.query.filter_by(is_deleted=False).all()
