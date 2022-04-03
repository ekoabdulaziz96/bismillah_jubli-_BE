from environs import Env
import logging

env = Env()
env.read_env()
# -------------------------------------------------------------------------------------
# --------------------------------------------------------------------- Config Flask
class Config:
    FLASK_APP = env.str("FLASK_APP", default="server.py")

    # flask-sqlalchemy config
    SQLALCHEMY_DATABASE_URI = env.str("SQLALCHEMY_DATABASE_URI", default=None)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask-caching config
    CACHE_TYPE = "RedisCache"       # Flask-Caching related configs
    CACHE_DEFAULT_TIMEOUT = 600     # seconds -> 10 minutes
    CACHE_REDIS_URL = env.str("CACHE_REDIS_URL", default=None)

    CELERY_TIMEZONE = env.str("CELERY_TIMEZONE", "Europe/Berlin")
    CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    CELERY_SEND_SENT_EVENT = True

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = env.str("MAIL_USERNAME", default=None)
    MAIL_PASSWORD = env.str("MAIL_PASSWORD", default=None)
    MAIL_DEFAULT_SENDER = env.str("MAIL_DEFAULT_SENDER", default=None)
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

class ProductionConfig(Config):
    ENV = 'production'
    DEVELOPMENT = False
    DEBUG = False
    LOG_LEVEL = logging.INFO

class StagingConfig(Config):
    ENV = 'staging'
    DEVELOPMENT = True
    DEBUG = True
    LOG_LEVEL = logging.INFO

class DevConfig(Config):
    ENV = 'development'
    DEVELOPMENT = True
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


# ---------------------------------- APP SETTING
app_settings = dict(
    production=ProductionConfig,
    staging=StagingConfig,
    development=DevConfig,
)
APP_SETTING = app_settings.get(env.str("FLASK_ENV", default="production"))
# --------------------------------------------------------------------- Set your config class goes here
