"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_caching import Cache

db: SQLAlchemy = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

cache = Cache()


# NOTE:
# flask_sqlalchemy      : https://flask-migrate.readthedocs.io/en/latest/
# flask_migrate         : https://flask-migrate.readthedocs.io/en/latest/
# flask_marshmallow     : https://flask-marshmallow.readthedocs.io/en/latest/
# flask_caching         : https://flask-caching.readthedocs.io/en/latest/
