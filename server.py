from app import create_app, make_celery, create_worker_app
# from cores import tasks
from services.tasks import workers

# ----------------------------- init app
app = create_app()
celery = make_celery(create_worker_app())

# ----------------------------- celery set method
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # import random
    # sender.add_periodic_task(5, workers.task_celery.s(inp=f'scheduled {random.randint(1,1000)}'), name='test-every-5')
    sender.add_periodic_task(30, workers.task_send_email.s(), name='scheduler-check-email-every-30-seconds')

# ----------------------------- route index
@app.route('/', methods=['GET'])
def index():
    print('print_log_core_notif')
    app.logger.debug('app_logger_debug_core_notif')
    app.logger.info('app_logger_info_core_notif')
    return 'core-notif', 200


@app.route('/test-celery', methods=['GET'])
def test_celery():
    print('print_log_core_notif')
    app.logger.debug('app_logger_debug_core_notif')
    app.logger.info('app_logger_info_core_notif')

    workers.task_send_email.delay()
    return 'test-celery', 200
