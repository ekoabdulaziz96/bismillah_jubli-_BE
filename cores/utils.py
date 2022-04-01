import pytz
import random
from datetime import datetime

def generate_api_call_id() -> str:
    """
    Generate unique api call id
    """
    current_date = datetime.now().strftime("%m%d%Y_%H%M%S")

    random_num = random.randint(1, 10000000)
    invoice_code = 'API_CALL_{}_{}'.format(str(current_date), str(random_num))

    return invoice_code

def get_timezone(timezone: str) -> pytz.timezone:
    """ get timezone
    :timezone -> timezone input, default "Asia/Jakarta"
    """
    try:
        tz = pytz.timezone(timezone)
        return tz
    except Exception:        # pragma: no cover
        return pytz.timezone('Asia/Jakarta')

def convert_datetime_to_specific_timezone(datetime: datetime, timezone: pytz.timezone) -> datetime:
    """ convert datetime obj saved in db to specific timezone
    :datetime -> datetime obj
    :timezone -> timezone obj
    """
    dt_utc = datetime.replace(tzinfo=pytz.UTC)      # replace method --> aware UTC
    dt_converted = dt_utc.astimezone(timezone)      # astimezone method --> convert to specific timezone

    return dt_converted
