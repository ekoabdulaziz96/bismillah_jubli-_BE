import traceback
from flask import (current_app as app)
from abc import (ABC, abstractmethod)

from cores import (utils, responses as respHelper, logs)

# ------------------------------------------------------------------------------ Parent Controller
class ParentController(ABC):
    """abstract class controller for handle request"""

    def __init__(self, request, timezone: str = 'Asia/Jakarta'):
        """ constructor for instance obj
        :request -> request object
        :timezone -> timezone that used
        """

        self.webapp = app
        self.request = request
        self.headers = request.headers if request.headers else {}

        self.timezone = timezone
        self.tz = utils.get_timezone(self.timezone)

        # init data
        self.is_valid = True
        self.add_data = dict()
        self.list_partial_process = []
        self.result = dict()

    # -------------------------------------------FUNCTION HELPER
    def _set_envinronment(self):
        """set envinronment variabel for controller class
        """
        self.response, self.status_code = respHelper.init_success_response(message_code=self.init_resp_message)
        self._do_process_log_request()

    def _do_process_log_request(self):
        """ process log request state
        """
        self.add_data['path'] = self.path
        self.log = logs.Log(activity=self.activity)
        self.log._process_log_request(request=self.request, add_data=self.add_data)

    def _do_process_log_processing(self, state: str, add_data: str):        # pragma: no cover
        """ process log processing state

        :state -> current state
        :add_data -> additional data for log
        """
        self.log._process_log_processing(state=state, add_data=add_data)

    def _do_process_log_response(self):
        """ process log response state
        """
        self.log._process_log_response(response=self.response, add_data=self.add_data)

    @abstractmethod
    def _set_list_partial_process(self):        # pragma: no cover
        """ set list partial process
        !must implemented
        !use variable self.list_partial_process with type `list`
        """
        print('not implemented yet')

    @abstractmethod
    def _do_process_db(self):         # pragma: no cover
        """ process to interact with db, like CRUD
        !must implemented
        """
        print('not implemented yet')

    @abstractmethod
    def _do_serialize_response(self):         # pragma: no cover
        """ process to serialaize data response to specific format/pattern
        !must implemented
        !use variable self.result_data with type `dict`
        """
        print('not implemented yet')

    def _set_exception_response(self, err: Exception):      # pragma: no cover
        """ Set response in exception scope
        :exception -> obj exception
        """
        self.webapp.logger.error(f"|{self.path}|------------------------------<Exception {self.activity}>")
        self.webapp.logger.error(err)
        self.webapp.logger.error(traceback.format_exc())
        self.webapp.logger.error(f"|{self.path}|------------------------------</Exception> {self.activity}\n")

        self.response, self.status_code = respHelper.process_response(self.response, action='error', message_code='GENERAL_ERROR_REQUEST')
        self.response.put("data", {'message': str(err)})

    # -------------------------------------------FUNCTION CONSUME
    def process(self):
        try:
            # update list partial process
            self._set_list_partial_process()

            # do partial process
            for partial_process in self.list_partial_process:
                partial_process()
                self.add_data[partial_process.__name__] = self.is_valid
                if self.is_valid is False:
                    return self.response, self.status_code

            # do process interact with db
            self._do_process_db()
            self.add_data[self._do_process_db.__name__] = self.is_valid

            # process serialize data
            self._do_serialize_response()
            self.add_data[self._do_serialize_response.__name__] = self.is_valid

            # update response data
            self.response.put('data', self.result_data)

        except Exception as err:
            self._set_exception_response(err)
        finally:
            self._do_process_log_response()

        # end try|except
        return self.response, self.status_code
# end class

# ------------------------------------------------------------------------------ Post Controller
class PostController(ParentController):
    """Controller class for handle request POST"""

    def __init__(self, request, timezone: str = 'Asia/Jakarta'):
        """ constructor for instance obj

        :request -> request object
        :timezone -> timezone that used
        """
        super().__init__(request, timezone)

        # init call method
        self._set_envinronment()

        # init variable
        self.payload = request.json if request.json else {}
        self.valid_payload = {}

        # self.schema = ...                 # set schema instance obj -> using in func `_process_validate_schema_for_payload_data`
        # self.serialize = ...              # set serializer instance obj -> using in func `_do_serialize_response`
        # self.instance_orm = ...           # set instance orm  -> using in func `_do_serialize_response`

    # -------------------------------------------FUNCTION HELPER
    def _process_validate_header_for_content_json(self):
        """validate content-type in header must be type json
        """
        if (self.headers.get('Content-Type', None) != "application/json"):
            self.response, self.status_code = respHelper.process_response(self.response, action="error", message_code="INVALID_HEADERS_JSON")
            self.is_valid = False

    def _process_validate_schema_for_payload_data(self):
        """validate schema for payload data
        """
        self.valid_payload = self.schema.load(self.payload)

    @abstractmethod
    def _process_normalize_valid_payload(self):         # pragma: no cover
        """ normalize valid payload to consume instance object
        !must implemented
        !data valid payload is in variable self.valid_payload with type `dict`
        """
        print('not implemented yet')

    # implement method
    def _set_list_partial_process(self):
        """ set list partial process
        !use variable self.list_partial_process with type `list`
        """
        self.list_partial_process = [
            self._process_validate_header_for_content_json,
            self._process_validate_schema_for_payload_data,
            self._process_normalize_valid_payload,
        ]

    # implement method
    def _do_serialize_response(self):
        """ process to serialaize data response to specific format/pattern
        """
        self.result_data = self.serialize.dump(self.instance_orm)

    # override method
    def _set_exception_response(self, err: Exception):
        """ Set response in exception scope
        :exception -> obj exception
        """
        self.webapp.logger.error(f"|{self.path}|------------------------------<Exception {self.activity}>")
        self.webapp.logger.error(err)
        self.webapp.logger.error(traceback.format_exc())
        self.webapp.logger.error(f"|{self.path}|------------------------------</Exception> {self.activity}\n")

        class_exc = type(err).__name__
        if class_exc == 'ValidationError':
            array_resp = respHelper.wrap_error_message_schema(dict(err.messages))
            self.response, self.status_code = respHelper.process_response(self.response, action='error', message_code='INVALID_REQUEST_PARAMETER')
            self.response.put("data", array_resp)
        else:       # pragma: no cover
            self.response, self.status_code = respHelper.process_response(self.response, action='error', message_code='GENERAL_ERROR_REQUEST')
            self.response.put("data", {'message': str(err)})

    # -------------------------------------------FUNCTION CONSUME
    # -
# end class
