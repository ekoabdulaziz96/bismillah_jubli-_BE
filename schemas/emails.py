import pytz
from datetime import datetime, timedelta
from marshmallow import (Schema, fields, validate, validates_schema, ValidationError)

from cores import (constants as const)
from models import (emails as mdlEmails)

# --------------------------------------------------------------------
# ---------------------------------------------STATIC VALUE
MESSAGE_POSITIVE_MIN_ONE = "input value must be greater than 0"
MESSAGE_INVALID_TIMESTAMP_FORMAT = "please check your Timestamp format `Day Month Year Hour:Minute`, ex: '15 Dec 2015 23:12'"
MESSAGE_INVALID_TIMESTAMP_VALUE = "please set the timestamp schedule at least 5 minutes earlier"

# -------------------------------------------------------------------- EMAILS
# -------------------------- CLASS SCHEMA
class EmailSchema(Schema):
    """ schema validation for validate payload create emails
    """
    event_id = fields.Integer(required=True, validate=validate.Range(min=1, error=MESSAGE_POSITIVE_MIN_ONE))
    email_subject = fields.Str(required=True, validate=validate.Length(max=mdlEmails.MAX_EMAIL_SUBJECT))
    email_content = fields.Str(required=True)

    timestamp = fields.DateTime(required=True, format=const.ConstEmail.FORMAT_TIMESTAMP, error_messages={"invalid": MESSAGE_INVALID_TIMESTAMP_FORMAT})

    @validates_schema
    def validate_is_available_timestamp(self, data, **kwargs):
        tz_singapore = pytz.timezone("Asia/Singapore")
        timestamp = data.get('timestamp', None)

        dt_utc = (timestamp - timedelta(hours=8)).replace(tzinfo=pytz.UTC)      # convert to UTC
        dt_singapore = dt_utc.astimezone(tz_singapore)                          # convert to singapore timezone

        dt_now = datetime.now(tz=tz_singapore)
        delta_dt = (dt_singapore - dt_now)
        days, hours, minutes = delta_dt.days, delta_dt.seconds // 3600, delta_dt.seconds // 60 % 60
        print(days, hours, minutes)
        if not(days >= 0 and (hours > 0 or minutes >= const.ConstEmail.THRESHOLD_TIMESTAMP)) is True:
            raise ValidationError(MESSAGE_INVALID_TIMESTAMP_VALUE, 'timestamp')
        else:
            data['timestamp'] = dt_utc

        return data
# end class

# ------------------------------------ CLASS SERIALIZER
class EmailSchemaSerializer(Schema):
    """ schema serializer email for response data
    """
    timestamp = fields.Function(lambda obj: (obj.timestamp + timedelta(hours=8)).strftime(const.ConstEmail.FORMAT_TIMESTAMP))
    status = fields.Function(lambda obj: obj.status.value if obj.status is not None else obj.status)

    class Meta:
        # Fields to expose
        fields = (
            'email_id',
            'event_id', 'email_subject', 'email_content', 'timestamp',
            'status'
        )
# end class
