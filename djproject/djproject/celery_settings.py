
import os
import re

# REDIS CONFIG
# celery, redis (auth access) configuration
BROKER_HOST_NAME = os.environ.get('BROKER_HOST_NAME')
REDIS_PASS = os.environ.get('REDIS_PASS')
REDIS_DB_NUMBER = os.environ.get('REDIS_DB_NUMBER')
REDIS_PORT = os.environ.get('REDIS_PORT')

# login credentials for RabbitMQ.
RPC_PASS = os.environ.get('RABBITMQ_DEFAULT_PASS')
RPC_USER = os.environ.get('RABBITMQ_DEFAULT_USER')
RPC_VHOST = os.environ.get('RABBITMQ_DEFAULT_VHOST')

# the host to which the rpc broker (rabbitmq) is deployed
RPC_HOST = os.environ.get('RABBITMQ_HOST')
RPC_PORT = os.environ.get('RABBITMQ_PORT', 5672)

# broker_url = 'amqp://myuser:mypassword@localhost:5672/myvhost'
_url = f'amqp://{RPC_USER}:{RPC_PASS}@{RPC_HOST}:{RPC_PORT}/{RPC_VHOST}'

broker_url = _url

result_persistent = True

# redis result backend
result_backend = f'redis://:{REDIS_PASS}@{BROKER_HOST_NAME}:{REDIS_PORT}/{REDIS_DB_NUMBER}'

imports = ('scrasync.tasks', 'scrasync.scraper', )

result_expires = 30
timezone = 'UTC'

accept_content = ['json', 'msgpack', 'yaml', 'pickle']

task_serializer = 'json'

result_serializer = 'json'

result_extended = True

task_routes = {
    re.compile(r'(data|container)\..*'): {'queue': 'rmxweb'},
    'scrasync.tasks.*': {'queue': 'scrasync'},
    'scrasync.scraper.*': {'queue': 'scrasync'},
}

RMXWEB_TASKS = {

    'create_from_webpage': 'data.tasks.create_from_webpage',

    'file_extract_callback': 'container.tasks.file_extract_callback',

    # todo(): delete this
    # 'push_many': 'crawl.tasks.push_many',
    # 'get_saved_endpoints': 'crawl.tasks.get_saved_endpoints',
    # 'delete_many': 'crawl.tasks.delete_many',
}
RMXWEB_QUEUE = 'rmxweb'

SCRASYSNC_TASKS = {

    # todo(): delete this
    # 'delete_many': 'scrasync.tasks.delete_many',

    'start_crawl': 'scrasync.scraper.start_crawl',

    'parse_and_save': 'scrasync.tasks.parse_and_save',
}

RMXWEB_QUEUE_NAME = 'rmxweb'

CELERY_GET_TIMEOUT = 5
