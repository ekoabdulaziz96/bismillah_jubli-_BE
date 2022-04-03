from celery import current_app as celery
from celery.utils.log import get_task_logger

from models.emails import (EmailQuery)
from services.modules.emails import (Email as moduleEmail)
logger = get_task_logger(__name__)


@celery.task
def task_celery(inp=None):       # pragma: no cover
    logger.debug('task_celery_log_debug')
    logger.info('task_celery_log_info')
    logger.info(f'input: {inp}')

@celery.task
def task_send_email():
    email_orm_list = EmailQuery.get_all_filter_by_current_datetime_tz_singapore()
    if len(email_orm_list) > 0:
        moduleEmail().process_send_email(email_orm_list=email_orm_list)
    else:
        logger.info('no email to process')

