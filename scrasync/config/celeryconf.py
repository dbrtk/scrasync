
# rabbitmq related imports
from .appconf import RPC_HOST, RPC_PASS, RPC_PORT, RPC_USER, RPC_VHOST

from .appconf import BROKER_HOST_NAME, REDIS_DB_NUMBER, REDIS_PASS, REDIS_PORT

# broker_url = 'amqp://myuser:mypassword@localhost:5672/myvhost'
_url = f'amqp://{RPC_USER}:{RPC_PASS}@{RPC_HOST}:{RPC_PORT}/{RPC_VHOST}'

broker_url = _url

result_persistent = True

result_backend = f'redis://:{REDIS_PASS}@{BROKER_HOST_NAME}:{REDIS_PORT}/{REDIS_DB_NUMBER}'

imports = ('scrasync.tasks', 'scrasync.scraper', )

result_expires = 30
timezone = 'UTC'

accept_content = ['json', 'msgpack', 'yaml', 'pickle']

task_serializer = 'json'

result_serializer = 'json'

result_extended = True

task_routes = {

    'scrasync.tasks.*': {'queue': 'scrasync'},
    'scrasync.scraper.*': {'queue': 'scrasync'},

    'rmxbot.tasks.*': {'queue': 'rmxbot'},

    'extractxt.tasks.*': {'queue': 'extractxt'},
}

RMXBOT_TASKS = {

    'create_data': 'rmxbot.tasks.data.create_from_webpage',

    'file_extract_callback': 'rmxbot.tasks.container.file_extract_callback',

}

