import traceback
from flask import (current_app as app)

class Log(object):
    """ class log for handle log data in request and response"""

    def __init__(self, activity: str):
        """ instantiation obj
        :app -> flask app
        :activity -> activity name , ex: CASHOUT
        """
        self.webapp = app
        self.activity = activity

        self._init_data()

    def _init_data(self):
        """init data log"""
        self.data_log = None
        self.activity_module = ''
        self.activity_name = ''
        self.state = ''

        self.req_method = ''
        self.req_url = ''
        self.payload = {}
        self.response = {}
        self.additional_data = {}

    def _do_print_log(self):
        """ print log """
        data_log = f"[{self.activity_module}][{self.activity_name}-{self.state}]"
        self.data_log = data_log + f" method: {self.req_method} || request: {self.req_url} ||"
        self.data_log += f" payload: {self.payload} || response: {self.response} || additional_data: {self.additional_data}"

        self.webapp.logger.info(f"--------------------------- < LOG {data_log} >")
        self.webapp.logger.info(f"{self.data_log}")
        self.webapp.logger.info(f"--------------------------- </ LOG {data_log} >")

    def _process_log_request(self, request: str, add_data: dict = {}):
        """ process log request data, before processed in controller

        :request -> flask.request
        :add_data -> additional data
        """
        try:
            body = request.json if request.json else {}

            self.activity_module = 'CORE-NOTIF'
            self.activity_name = self.activity
            self.state = 'REQUEST'
            self.req_method = request.method
            self.req_url = request.url
            self.payload = body
            self.additional_data = add_data

            # do print log
            self._do_print_log()

        except Exception as err:    # pragma: no cover
            self.webapp.logger.error('---------ERROR PROCESS LOG REQUEST---------')
            self.webapp.logger.error(err)
            self.webapp.logger.error(traceback.format_exc())

    def _process_log_processing(self, state: str, add_data: dict = {}):     # pragma: no cover
        """ process log response data, after processed in controller

        :state -> message id
        :add_data -> additional data
        """
        try:
            self.state = 'PROCESSING_' + state
            self.additional_data = add_data

            # do print log
            self._do_print_log()

        except Exception as err:    # pragma: no cover
            self.webapp.logger.error('---------ERROR PROCESS LOG PROCESSING---------')
            self.webapp.logger.error(err)
            self.webapp.logger.error(traceback.format_exc())

    def _process_log_response(self, response, add_data: dict = {}):
        """ process log response data, after processed in controller

        :response -> Response obj
        """
        try:
            self.state = 'RESPONSE'
            self.response = response.stringify_v1()
            self.additional_data = add_data

            # do print log
            self._do_print_log()

        except Exception as err:    # pragma: no cover
            self.webapp.logger.error('---------ERROR PROCESS LOG RESPONSE---------')
            self.webapp.logger.error(err)
            self.webapp.logger.error(traceback.format_exc())
