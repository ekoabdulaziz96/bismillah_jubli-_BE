from .emails import Email
from .user_recipients import UserRecipient
from .email_histories import EmailHistory

# register your table here
register_tables = {
    "Email": Email,
    "UserRecipient": UserRecipient,
    "EmailHistory": EmailHistory
}
