from celery import current_app as celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery.task
def task_celery(inp=None):
    logger.debug('task_celery_log_debug')
    logger.info('task_celery_log_info')
    logger.info(f'input: {inp}')
