
BROKER_URL = 'redis://localhost:6379/0',
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_IMPORTS = ('scrasync.tasks', )

CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

