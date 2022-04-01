import json
import random
import string
from datetime import datetime
from unittest import (TestCase)

import server
from cores import (responses as respHelper, databases)


# create your own parent unittest here or inherit then put your own version 1,2,3
# ex : ParentTestServicesV2
# -------------------------------------------------------------
# -------------------------------------------------------PARENT TEST CASE
class ParentTestCase(TestCase):
    """== Class parent unittest to set init config == \n
    """
    @classmethod
    def setUpClass(cls):
        """ call once a time """
        super(ParentTestCase, cls).setUpClass()
        # instance app Flask and client
        cls.app = server.app
        # cls.app.debug = True
        cls.client = cls.app.test_client()

        # instance db sqlalchemy
        cls.db = databases.db
        cls.db.app = cls.app

        cls.init_response, cls.init_status_code = respHelper.init_success_response(message_code='INIT_SUCCESS')
# end class

# -------------------------------------------------------------
# -------------------------------------------------------PARENT TEST SERVICES
class ParentTestService(object):
    """== Class parent test service with helper method == \n
        Scenario Test
        - [..]
        - [..]

        -----
        Note:
        1. [+] for positive test || [-] for negative test
        2. please makse sure, if inherit this class you must set a few attr:
            - self.req_method --> request method that used ['GET', 'POST', 'PUT', 'DELETE']
            - self.url: url
            - self.payload: dict
            - self.headers: dict
                (if not using headers, then set self.headers = None)
            - self.init_response: class Response (path: cores/responses.py)
            - self.init_serialize: dict
                (key with default or empty value. Also you can assign it with {})
                (used in function _doPostFailTestAndValidate & _doGetFailTestAndValidate)
        3. best practice for this parent class only handle a single endpoint
    """
    @classmethod
    def getRandomString(cls, length: int):
        """ return random string with size length :param `length`(int)"""

        random_str = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
        return random_str

    def _doGet(self):        # pragma: no cover
        """ to make request GET with specific url and also data headers (if exist)
        """
        response = self.client.get(self.url, headers=self.headers)
        # breakpoint()
        return response

    def _doPost(self):
        """ to make request POST with specific url, data payload and also data headers (if exist)
        """
        data = json.dumps(self.payload)
        response = self.client.post(self.url, headers=self.headers, data=data)
        # breakpoint()
        return response

    def _doPut(self):        # pragma: no cover
        """ to make request POST with specific url, data payload and also data headers (if exist)
        """
        data = json.dumps(self.payload)
        response = self.client.put(self.url, headers=self.headers, data=data)
        # breakpoint()
        return response

    def _doPatch(self):      # pragma: no cover
        """ to make request PATCH with specific url, data payload and also data headers (if exist)
        """
        data = json.dumps(self.payload)
        response = self.client.patch(self.url, headers=self.headers, data=data)
        # breakpoint()
        return response

    # ----- add your req method here

    def _validateResponse(self, currentResponse: dict, expectResponse: dict):
        """
        comparare :param `currentResponse`(dict) with :param `expectResponse`(dict) to validate the equality.
        note : message_data value isn't validate yet, you must create it based on test case scenario
        """

        # validate count key/data
        self.assertEqual(len(currentResponse), len(expectResponse))

        # validate key is exist
        self.assertIn('message_action', currentResponse)
        self.assertIn('message_desc', currentResponse)
        self.assertIn('message_data', currentResponse)
        self.assertIn('message_id', currentResponse)
        self.assertIn('message_request_datetime', currentResponse)

        # validate value , except message_data
        self.assertEqual(currentResponse.get('message_action'), expectResponse.get('message_action'))
        self.assertEqual(currentResponse.get('message_desc'), expectResponse.get('message_desc'))
        # not provide validate value message_data
        self.assertEqual(currentResponse.get('message_id')[:8], 'API_CALL')
        currDatetime = type(datetime.fromisoformat(currentResponse.get('message_request_datetime')))
        self.assertEqual(currDatetime, datetime)

    def _assertInForKeys(self, loopKeyData: list, expectData: dict):
        """ check all key of :param `loopKeyData`(dict) is exist in :param `expectData`(dict) """

        for key in loopKeyData:
            self.assertIn(key, expectData)

    def _assertNotInForKeys(self, loopKeyData: list, expectData: dict):
        """ check all key of :param `loopKeyData`(dict) is not exist in :param `expectData`(dict) """

        for key in loopKeyData:
            self.assertNotIn(key, expectData)

    def _doTestAndValidateExceptMessageData(self, test: str, message_code: str):
        """
        do scenario test to make request with specific url and also data headers (if exist)
        then validate response result (except message_data) based on criteria type :param `test`(str) and :param `message_code`(str).

        :test --> test type ['success', 'error']
        :message_code --> key of dict (path: cores/messages.py)
        """

        # prepare data
        expectResponse, expectStatusCode = respHelper.process_response(self.init_response, action=test, message_code=message_code)

        req_method_dict = dict(
            GET=self._doGet,
            POST=self._doPost,
            PUT=self._doPut,
            PATCH=self._doPatch,
            # Delete=self._doDelete,
        )
        # do get request
        response = req_method_dict.get(self.req_method)()
        currResponse = response.json

        # validate status code
        self.assertEqual(response.status_code, expectStatusCode)
        # validate response structure and detail data (except message_data)
        self._validateResponse(currResponse, expectResponse.stringify_v1())

        return currResponse

    def _doFailTestAndValidate(self, err_message_code: str):
        """
        do scenario FAIL test to make request with specific url and also data headers (if exist)
        then validate response result based on criteria :param `message_code`(str).

        :err_message_code --> error message key of dict (path: cores/messages.py)
        """

        currResponse = self._doTestAndValidateExceptMessageData(test='error', message_code=err_message_code)
        # validate response message_data
        self.assertEqual(currResponse.get('message_data'), {})
        self._assertNotInForKeys(loopKeyData=self.init_serialize, expectData=currResponse.get('message_data'))
# end class

# -------------------------------------------------------PARENT POST TEST SERVICES
class ParentPostTestService(ParentTestService):
    """== Class parent post test service with helper method and test header json == \n
        Scenario Test
        - [-] Content-Type in header is not sended
        - [-] Content-Type in header is not correct for json syntax  ("application/json")
        -----
        Note:
        1. [+] for positive test || [-] for negative test || [...]P for common test function and written in parent
        2. please makse sure, if inherit this class you must set a few attr:
            - self.url: url
            - self.payload: dict
            - self.headers: dict
                (if not using headers, then set self.headers = None)
            - self.init_response: class Response (path: cores/responses.py)
            - self.init_serialize: dict
                (key with default or empty value. Also you can assign it with {})
                (used in function _doPostFailTestAndValidate & _doGetFailTestAndValidate)
        3. best practice for this parent class only handle a single endpoint
    """
    # -----------------------------------------------------------------------------
    # -------------------------------------------------------------FUNCTION CONSUME
    def test_with_content_type_in_header_is_not_sended(self):
        # prepare data
        key = 'Content-Type'
        del self.headers[key]

        self._doFailTestAndValidate(err_message_code='INVALID_HEADERS_JSON')

    def test_with_content_type_in_header_is_not_correct_for_json_syntax(self):
        # prepare data
        key = 'Content-Type'
        self.headers[key] = 'JSON'

        self._doFailTestAndValidate(err_message_code='INVALID_HEADERS_JSON')
# end class
