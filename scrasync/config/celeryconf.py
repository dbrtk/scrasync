
from .appconf import BROKER_HOST_NAME, REDIS_PASS


_url = f'redis://:{REDIS_PASS}@{BROKER_HOST_NAME}:6379/0'

BROKER_URL = _url
CELERY_RESULT_BACKEND = _url


CELERY_IMPORTS = ('scrasync.tasks', 'scrasync.scraper', )

CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_ROUTES = {

    'scrasync.tasks.*': {'queue': 'scrasync'},
    'scrasync.scraper.*': {'queue': 'scrasync'},

    'rmxbot.tasks.*': {'queue': 'rmxbot'},

    'extractxt.tasks.*': {'queue': 'extractxt'},
}

RMXBOT_TASKS = {

    'create_data': 'rmxbot.tasks.data.create_from_webpage',

    'file_extract_callback': 'rmxbot.tasks.container.file_extract_callback',

}

