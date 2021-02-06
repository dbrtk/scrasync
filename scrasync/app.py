
from celery import Celery

from scrasync.config import celeryconf


celery = Celery('scrasync')
celery.config_from_object(celeryconf)
celery.control.add_consumer('scrasync', reply=True)
