from flask import (Blueprint, request)
# from flask import current_app as app
from cores import (constants as const)
from services.controllers import (emails as ctrlEmails)

# ------------------------------------------- init blueprint
bp_emails = Blueprint('emails', __name__)

# ------------------------------------------- route
@bp_emails.route(const.ConstRouteEmail.SAVE_EMAIL, methods=["POST"])
def email_save():

    email_save_obj = ctrlEmails.EmailSave(request)
    response, status_code = email_save_obj.process()

    return response.stringify_v1(), status_code
