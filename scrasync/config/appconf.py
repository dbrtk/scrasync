
import os

__HERE = os.path.abspath(__file__)


DATA_FOLDER = os.path.abspath(os.path.join(
    __HERE, os.pardir, os.pardir, os.pardir, 'data'))

USER_AGENTS_FILE = os.path.join(DATA_FOLDER, 'user-agents.txt')

PROXIMITY_USER = 'username'

HTTP_TIMEOUT = 10


# acceptable content_type
TEXT_C_TYPES = ['text/plain', 'text/html']


# the maximal amount of pages per crawl/container
CRAWL_MAX_PAGES = 500

# AIOHTTP CONFIG
AIOHTTP_MAX_URLS = 25


# REDIS CONFIG
# celery, redis (auth access) configuration
BROKER_HOST_NAME = os.environ.get('BROKER_HOST_NAME')
REDIS_PASS = os.environ.get('REDIS_PASS')
REDIS_DB_NUMBER = os.environ.get('REDIS_DB_NUMBER')
REDIS_PORT = os.environ.get('REDIS_PORT')


# the expiration time is set to one hour.
REDIS_EXPIRATION_TIME = 60 * 60


# the size of the buffer for reading responses streamed by aiohttp.
AIOHTTP_BUFSIZE = 8 * 1024

# RabbitMQ configuration
# RabbitMQ rpc queue name
# These values are defined on the level of docker-compose.
RPC_QUEUE_NAME = os.environ.get('RPC_QUEUE_NAME', 'scrasync')

# login credentials for RabbitMQ.
RPC_PASS = os.environ.get('RABBITMQ_DEFAULT_PASS')
RPC_USER = os.environ.get('RABBITMQ_DEFAULT_USER')
RPC_VHOST = os.environ.get('RABBITMQ_DEFAULT_VHOST')

# the host to which the rpc broker (rabbitmq) is deployed
RPC_HOST = os.environ.get('RABBITMQ_HOST')
RPC_PORT = os.environ.get('RABBITMQ_PORT', 5672)
RABBITMQ_METRICS_PORT = os.environ.get('RABBITMQ_METRICS_PORT')
RABBITMQ_SCRASYNC_QUEUES_NAME = os.environ.get('RABBITMQ_SCRASYNC_QUEUES_NAME')

# configurations for mongodb crawl status
MONGO_RPC_DATABASE = os.environ.get('MONGO_RPC_DATABASE')
MONGO_CRAWL_STATE_COLL = os.environ.get('MONGO_CRAWL_STATE_COLL')
MONGO_CRAWL_RESULTS_COLL = os.environ.get('MONGO_CRAWL_RESULTS_COLL')

MONGO_RPC_USER = os.environ.get('MONGO_RPC_USER')
MONGO_RPC_PASS = os.environ.get('MONGO_RPC_PASS')
MONGODB_LOCATION = os.environ.get('MONGODB_LOCATION')
MONGO_PORT = os.environ.get('MONGO_PORT')

# prometheus settings 
PROMETHEUS_HOST = os.environ.get('PROMETHEUS_HOST')
PROMETHEUS_PORT = os.environ.get('PROMETHEUS_PORT')
PROMETHEUS_PATH = os.environ.get('PROMETHEUS_PATH')

