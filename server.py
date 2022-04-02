from app import create_app, shell_plus_command

from cores.extensions import make_celery
# from cores import tasks
from services.tasks import workers

# ----------------------------- init app
app = create_app()
app.cli.add_command(shell_plus_command)

celery = make_celery(app)

# ----------------------------- set scheduled task
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    import random
    sender.add_periodic_task(5, workers.task_celery.s(inp=f'scheduled {random.randint(1,1000)}'), name='test-every-5')

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

    workers.task_celery.delay()
    return 'test-celery', 200

# -------------------------------------------
# see folder ./urls for more route app endpoint
