
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
# redis db host
BROKER_HOST_NAME = os.environ.get('BROKER_HOST_NAME')
REDIS_HOST_NAME = os.environ.get('REDIS_HOST_NAME')


# the expiration time is set to one hour.
REDIS_EXPIRATION_TIME = 60 * 60


# the size of the buffer for reading responses streamed by aiohttp.
AIOHTTP_BUFSIZE = 8 * 1024


# celery, redis (auth access) configuration
REDIS_PASS = os.environ.get('REDIS_PASS')
REDIS_DB_NUMBER = 0
REDIS_PORT = 6379


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

# mongodb celery backend
DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
MONGO_PORT = os.environ.get('MONGO_PORT')
MONGODB_LOCATION = os.environ.get('MONGODB_LOCATION')
RPC_DATABASE = os.environ.get('RPC_DATABASE')
RPC_COLLECTION = os.environ.get('RPC_COLLECTION')
