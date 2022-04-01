import random
import string

# create your own parent unittest here or inherit then put your own version 1,2,3
# ex : ParentUnittestSchemasV2
# -------------------------------------------------------------
# ---------------------------------------------------PARENT TEST SCHEMA
class ParentTestSchema(object):
    """ == Parent Test Schema with helper function and common test case == \n
        Scenario Test
        - [+] test payload with all field (include optional field)
        - [+] test payload with only mandatory field
        - [-] test payload without data
        - [-] test payload with unregistered key
        -----
        Note: [+] for positive test || [-] for negative test
    """
    # constant data
    err_message_missing_required = 'Missing data for required field.'
    err_message_unknown_field = 'Unknown field.'
    err_message_max_length = 'Longer than maximum length maxLength.'
    err_message_min_length = 'Longer than minimum length minLength.'
    err_message_invalid_bool = 'Not a valid boolean.'
    err_message_null_field = 'Field may not be null.'

    # ------------------------------------------------------------
    # --------------------------------------------function helper
    @classmethod
    def getRandomString(cls, length: int):
        """ return random string with size length :param `length`(int)"""

        random_str = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
        return random_str

    def _loopAssertInForKeys(self, loopKeyData: dict, expectData: dict):
        """ check all key of :param `loopKeyData`(dict) is exist in :param `expectData`(dict) """

        for key in loopKeyData.keys():
            self.assertIn(key, expectData)

    def _loopAssertEqual(self, currData: dict, expectData: dict):
        """ check value :param `currData`(dict) is equal to value in :param `expectData`(dict) based on specific key """

        for key in currData.keys():
            self.assertEqual(currData.get(key), expectData.get(key))

    def _invalidMinLengthPayload(self, key: str, minLength: int):       # pragma: no cover
        """ do scenario with error invalid min length :param `minLength`(int) for specific :param `key`(str) in payload """

        data = self.payload_full.copy()
        data[key] = self.getRandomString(minLength - 1)

        with self.assertRaises(Exception) as context:
            self.schema.load(data)
        err = context.exception.messages

        # count error data
        self.assertEqual(len(err), 1)
        # check error key and value in schema
        self.assertTrue(key in err)
        self.assertEqual(err.get(key)[0], self.err_message_max_length.replace('maxLength', str(minLength)))

    def _invalidMaxLengthPayload(self, key: str, maxLength: int):
        """ do scenario with error invalid max length :param `maxLength`(int) for specific :param `key`(str) in payload """

        data = self.payload_full.copy()
        data[key] = self.getRandomString(maxLength + 1)

        with self.assertRaises(Exception) as context:
            self.schema.load(data)
        err = context.exception.messages

        # count error data
        self.assertEqual(len(err), 1)
        # check error key and value in schema
        self.assertTrue(key in err)
        self.assertEqual(err.get(key)[0], self.err_message_max_length.replace('maxLength', str(maxLength)))

    def _invalidValidatePayload(self, data: dict, key: str, err_message: str):
        """ do scenario with specific error based on :param `err_message`(str) for specific :param `key`(str) in payload """

        with self.assertRaises(Exception) as context:
            self.schema.load(data)
        err = context.exception.messages

        # count error data
        self.assertEqual(len(err), 1)
        # check error key and value in schema
        self.assertTrue(key in err)
        self.assertEqual(err.get(key)[0], err_message)

    def _invalidValidateNestedManyPayload(self, payload: dict, nested_key: str, key: str, err_message: str):         # pragma: no cover
        """ do scenario with specific error in nested schema
        :payload -> payload data input
        :nested_key -> nested_key name
        :key -> key name that used for err test
        :err_message -> expect error message
        """

        with self.assertRaises(Exception) as context:
            self.schema.load(payload)
        err = context.exception.messages
        err_nested = err.get(nested_key, None)
        # count error data
        self.assertEqual(len(err), 1)
        # check error key and value in schema
        self.assertTrue(key in err_nested[0])
        self.assertEqual(err_nested[0].get(key)[0], err_message)

    # -------------------------------------------------------------
    # --------------------------------------------function consume / test
    def test_payload_with_all_field(self):
        valid_data = self.schema.load(self.payload_full)

        # check count valid data
        self.assertEqual(len(valid_data), len(self.payload_full))
        # check key in valid data
        self._loopAssertInForKeys(loopKeyData=valid_data, expectData=self.payload_full)
        # check value in valid data
        self._loopAssertEqual(currData=valid_data, expectData=self.payload_full)

    def test_payload_with_only_mandatory_field(self):
        valid_data = self.schema.load(self.payload_mandatory_only)

        # check count valid data
        self.assertEqual(len(valid_data), len(self.payload_mandatory_only))
        # check key in valid data
        self._loopAssertInForKeys(loopKeyData=valid_data, expectData=self.payload_mandatory_only)
        # check value in valid data
        self._loopAssertEqual(currData=valid_data, expectData=self.payload_mandatory_only)

    def test_payload_without_data(self):
        payload_invalid = dict()

        with self.assertRaises(Exception) as context:
            self.schema.load(payload_invalid)
        err = context.exception.messages

        # check count err data message
        self.assertEqual(len(err), len(self.payload_mandatory_only))
        # check key in err data
        self._loopAssertInForKeys(loopKeyData=err, expectData=self.payload_mandatory_only)
        # check error message
        for key in self.payload_mandatory_only.keys():
            self.assertEqual(err.get(key)[0], self.err_message_missing_required)

    def test_payload_with_unregistered_key(self):
        payload_invalid = self.payload_full.copy()
        payload_invalid['unregistered_key'] = 'unregistered_value'

        with self.assertRaises(Exception) as context:
            self.schema.load(payload_invalid)
        err = context.exception.messages

        # count error data
        self.assertEqual(len(err), len(payload_invalid) - len(self.payload_full))
        # check error unregistered key and value in schema
        self.assertTrue('unregistered_key' in err)
        self.assertEqual(err.get('unregistered_key')[0], self.err_message_unknown_field)
