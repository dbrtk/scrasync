import os

from celery import Celery

from scrasync.config import celeryconf

# os.environ['REDIS_HOST_NAME'] = 'localhost'


celery = Celery('scrasync')
celery.config_from_object(celeryconf)
