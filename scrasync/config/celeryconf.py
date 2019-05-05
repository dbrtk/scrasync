
BROKER_URL = 'redis://localhost:6379/0',
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

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
}

RMXBOT_TASKS = {

    'create_data': 'rmxbot.tasks.data.call_data_create'
}