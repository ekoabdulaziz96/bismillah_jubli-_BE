from cores import (responses as respHelper)
from models.emails import (Email as mdlEmail, EmailStatusChoices, EmailQuery)
from schemas import (emails as schEmails)
from ..parents.controllers import (PostController)


# ----------------------------------------------------Prepare constant data
PATH = "services/controllers/emails"
SERVICE = 'EMAIL'

# -----------------------------------------------CONTROLLER CLASS
class EmailSave(PostController):
    """ class controller for save data Email
    """
    path = PATH
    activity = f'{SERVICE}_SAVE'
    init_resp_message = "SUCCESS_CREATE"

    def __init__(self, request, timezone: str = 'Asia/Jakarta'):
        """ constructor for instance obj

        :request -> request object
        :timezone -> timezone that used
        """
        super().__init__(request, timezone)

        # init variable
        self.schema = schEmails.EmailSchema()
        self.serialize = schEmails.EmailSchemaSerializer()

    # -------------------------------------------FUNCTION HELPER
    # implement method
    def _process_normalize_valid_payload(self):
        """ normalize valid payload to consume instance object
        """
        self.event_id = self.valid_payload.get('event_id', None)
        self.email_subject = self.valid_payload.get('email_subject', None)
        self.email_content = self.valid_payload.get('email_content', None)
        self.timestamp = self.valid_payload.get('timestamp', None)

    def _process_validate_is_event_id_exist(self):
        """process validate is event_id exist or not"""

        if EmailQuery.get_one_filter_by_event_id(event_id=self.event_id) is not None:
            self.is_valid = False
            self.response, self.status_code = respHelper.process_response(self.response, action="error", message_code='EVENT_ID_ALREADY_EXIST')

    # override method
    def _set_list_partial_process(self):
        """ set list partial process
        """
        super()._set_list_partial_process()
        self.list_partial_process += [
            self._process_validate_is_event_id_exist,
        ]

    # implement method
    def _do_process_db(self):
        """ process to interact with db -> create new data in db for table emails
        """
        payload = dict(
            event_id=self.event_id,
            email_subject=self.email_subject,
            email_content=self.email_content,
            timestamp=self.timestamp,

            status=EmailStatusChoices.OPEN
        )
        self.instance_orm = mdlEmail(**payload)
        self.instance_orm.save()
        self.add_data['instance_orm'] = self.instance_orm

    # -------------------------------------------FUNCTION CONSUME
    # -
# end class
