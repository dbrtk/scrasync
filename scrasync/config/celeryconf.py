
from .appconf import REDIS_HOST_NAME

BROKER_URL = 'redis://{}:6379/0'.format(REDIS_HOST_NAME)
CELERY_RESULT_BACKEND = 'redis://{}:6379/0'.format(REDIS_HOST_NAME)

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

    'file_extract_callback': 'rmxbot.tasks.corpus.file_extract_callback',

}
EXTRACTXT_TASKS = {

    'extract_from_txt': 'extractxt.tasks.extract_from_txt',
}

