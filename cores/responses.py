import copy
import datetime
from typing import Dict

from cores.utils import (generate_api_call_id, get_timezone)
from cores.messages import (RESPONSE_ERROR, RESPONSE_SUCCESS)

class Response():
    mapping_data = dict(
        status='message_action',
        desc='message_desc',
        data='message_data',
    )

    def __init__(self, status, desc, data, timezone='Asia/Jakarta'):
        call_id = generate_api_call_id()

        tz = get_timezone(timezone)
        date_time_obj = datetime.datetime.now(tz)

        self.response = dict(
            id=call_id,
            status=status,
            desc=desc,
            data=data,
            message_id=call_id,
            message_action=status,
            message_desc=desc,
            message_data=data,
            message_request_datetime=date_time_obj.strftime('%Y-%m-%d %H:%M:%S'),
        )

    def put(self, key, value):
        if not (key in self.response):           # pragma: no cover
            raise ValueError('SETTING_NON_EXISTING_FIELD', key, value)

        self.response[key] = value
        self.response[self.mapping_data[key]] = value

    def stringify_v1(self):
        record_prev = copy.deepcopy(self.response)
        del record_prev['status']
        del record_prev['id']
        del record_prev['desc']
        del record_prev['data']
        return record_prev


def wrap_error_message_schema(err_messages: Dict):
    array_resp = list()
    for key, value in err_messages.items():
        err_dict = dict(
            key=key,
            description=value[0] if type(value) == list else value
        )
        array_resp.append(err_dict)

    return array_resp

def process_response(response: Response, action: str, message_code: str):
    resp_config = dict()
    status_code = 200

    if action == 'success':
        resp_config = RESPONSE_SUCCESS.get(message_code)
    if action == 'error':
        resp_config = RESPONSE_ERROR.get(message_code)

    if resp_config:
        response.put('status', resp_config.get('code'))
        response.put('desc', resp_config.get('message'))
        status_code = resp_config.get('status')

    return response, status_code

def init_success_response(message_code: str, timezone: str = 'Asia/Jakarta'):
    init_resp = Response("", "", {}, timezone)

    response, status_code = process_response(init_resp, action='success', message_code=message_code)

    return response, status_code
