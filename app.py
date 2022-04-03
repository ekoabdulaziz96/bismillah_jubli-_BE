from celery import Celery

from flask import Flask
from cores import (config, extensions)
from models.register_tables import (register_tables)
from urls.register_routers import (bp_emails)

def create_app():
    """
    Create application factory,
    as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config.APP_SETTING)
    app.logger.setLevel(config.APP_SETTING.LOG_LEVEL)
    register_blueprints(app)
    register_extensions(app)
    register_shellcontext(app)

    return app

def create_worker_app():
    """create worker app without blueprint"""
    app = Flask(__name__)
    app.config.from_object(config.APP_SETTING)
    app.logger.setLevel(config.APP_SETTING.LOG_LEVEL)
    register_extensions(app)
    register_shellcontext(app)

    return app

def register_extensions(app):
    """Register Flask extensions."""
    extensions.db.init_app(app)
    extensions.migrate.init_app(app, extensions.db)
    extensions.ma.init_app(app)
    extensions.cache.init_app(app)
    extensions.mail.init_app(app)

    return None

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(bp_emails)
    return None

def register_shellcontext(app):
    """Register shell context objects."""
    shell_context = {'db': extensions.db}
    shell_context.update(register_tables)

    app.shell_context_processor(lambda: shell_context)

def make_celery(app):
    celery = Celery(
        'core_notif',
        broker=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        include=['services.tasks.workers'],
        enable_utc=True,
        timezone=app.config['CELERY_TIMEZONE']
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
