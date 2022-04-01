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
