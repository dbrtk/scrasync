
import os

from celery import Celery

from . import celery_settings


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djproject.settings')

celery = Celery('scrasync')
celery.config_from_object(celery_settings)

celery.autodiscover_tasks()
