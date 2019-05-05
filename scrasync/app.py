import os

from celery import Celery
from flask import Flask
from werkzeug.routing import BaseConverter

from scrasync.config import celeryconf

os.environ['REDIS_HOST_NAME'] = 'localhost'


class ObjectidConverter(BaseConverter):
    """A url converter for bson's ObjectId."""

    regex = r"[a-f0-9]{24}"


def create_app():
    """Building up the flask applicaiton."""
    app = Flask(__name__)

    app.url_map.converters['objectid'] = ObjectidConverter

    with app.app_context():
        from .routes import scrasync_app

        app.register_blueprint(scrasync_app)

    return app


celery = Celery('scrasync')
celery.config_from_object(celeryconf)

