"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_caching import Cache
from celery import Celery


db: SQLAlchemy = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

cache = Cache()

def make_celery(app):
    celery = Celery(
        'core_notif',
        broker=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        include=['services.tasks.workers', 'services.tasks.schedulers'],
        enable_utc=True,
        timezone=app.config['CELERY_TIMEZONE']
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


# NOTE:
# flask_sqlalchemy      : https://flask-migrate.readthedocs.io/en/latest/
# flask_migrate         : https://flask-migrate.readthedocs.io/en/latest/
# flask_marshmallow     : https://flask-marshmallow.readthedocs.io/en/latest/
# flask_caching         : https://flask-caching.readthedocs.io/en/latest/
# celery                : https://docs.celeryq.dev/en/stable/index.html
