import os

from celery import Celery
from flask import Flask
from werkzeug.routing import BaseConverter

from .config import celeryconf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'data')
STATIC_FOLDER = os.path.join(BASE_DIR, 'static', 'rmx')

os.environ['RMX_SEARCH_CORPUS_SCRIPT'] = os.path.join(BASE_DIR, 'bin')
os.environ['NLP_ENDPOINT'] = 'http://localhost:8001'
os.environ['SCRASYNC_ENDPOINT'] = 'http://localhost:8002'
os.environ['EXTRACTXT_ENDPOINT'] = 'http://localhost:8003'

os.environ['DATA_ROOT'] = DATA_ROOT
os.environ['TMP_DATA_DIR'] = os.path.join(DATA_ROOT, 'tmp')
os.environ['MONGODB_LOCATION'] = 'localhost'
os.environ['REDIS_HOST_NAME'] = 'localhost'
os.environ['TEMPLATES_FOLDER'] = os.path.join(BASE_DIR, 'templates')


class ObjectidConverter(BaseConverter):
    """A url converter for bson's ObjectId."""

    regex = r"[a-f0-9]{24}"


def create_app():
    """Building up the flask applicaiton."""
    app = Flask(__name__)

    app.url_map.converters['objectid'] = ObjectidConverter

    # from rmxbot.contrib.rmxjson import RmxEncoder
    # app.json_encoder = RmxEncoder

    # app.config.from_object('conf')
    # app.config.update(
    #     BROKER_URL='redis://localhost:6379/0',
    #     CELERY_RESULT_BACKEND='redis://localhost:6379/0'
    # )

    with app.app_context():
        from .routes import scrasync_app

        app.register_blueprint(scrasync_app)

    return app


celery = Celery('scrasync')
celery.config_from_object(celeryconf)
