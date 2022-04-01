from datetime import timedelta

from marshmallow import (Schema, fields, validate)
from models import (emails as mdlEmails)

# --------------------------------------------------------------------
# ---------------------------------------------STATIC VALUE
MESSAGE_POSITIVE_MIN_ONE = "input value must be greater than 0"
MESSAGE_INVALID_TIMESTAMP = "please check your Timestamp format `Day Month Year Hour:Minute`, ex: '15 Dec 2015 23:12'"
# -------------------------------------------------------------------- EMAILS
# -------------------------- CLASS SCHEMA
class EmailSchema(Schema):
    """ schema validation for validate payload create emails
    """
    event_id = fields.Integer(required=True, validate=validate.Range(min=1, error=MESSAGE_POSITIVE_MIN_ONE))
    email_subject = fields.Str(required=True, validate=validate.Length(max=mdlEmails.MAX_EMAIL_SUBJECT))
    email_content = fields.Str(required=True)

    timestamp = fields.DateTime(required=True, format="%d %b %Y %H:%M", error_messages={"invalid": MESSAGE_INVALID_TIMESTAMP})

# end class

# ------------------------------------ CLASS SERIALIZER
class EmailSchemaSerializer(Schema):
    """ schema serializer email for response data
    """
    timestamp = fields.Function(lambda obj: (obj.timestamp + timedelta(hours=8)).strftime('%d %b %Y %H:%M'))
    status = fields.Function(lambda obj: obj.status.value if obj.status is not None else obj.status)

    class Meta:
        # Fields to expose
        fields = (
            'email_id',
            'event_id', 'email_subject', 'email_content', 'timestamp',
            'status'
        )
# end class
