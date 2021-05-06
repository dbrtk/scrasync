
import os

__HERE = os.path.abspath(__file__)

# todo(): delete this.
# DATA_FOLDER = os.path.abspath(os.path.join(
#     __HERE, os.pardir, os.pardir, os.pardir, 'data'))

USER_AGENTS_FILE = os.path.join(
    os.environ.get('PATH_TO_DATA', ''), 'user-agents.txt')

HTTP_TIMEOUT = 10


# acceptable content_type
TEXT_C_TYPES = ['text/plain', 'text/html']


# the maximal amount of pages per crawl/container
CRAWL_MAX_PAGES = 500


# REDIS CONFIG
# celery, redis (auth access) configuration
# todo(): delete celery variables
# BROKER_HOST_NAME = os.environ.get('BROKER_HOST_NAME')
# REDIS_PASS = os.environ.get('REDIS_PASS')
# REDIS_DB_NUMBER = os.environ.get('REDIS_DB_NUMBER')
# REDIS_PORT = os.environ.get('REDIS_PORT')
#
# # login credentials for RabbitMQ.
# RPC_PASS = os.environ.get('RABBITMQ_DEFAULT_PASS')
# RPC_USER = os.environ.get('RABBITMQ_DEFAULT_USER')
# RPC_VHOST = os.environ.get('RABBITMQ_DEFAULT_VHOST')
#
# # the host to which the rpc broker (rabbitmq) is deployed
# RPC_HOST = os.environ.get('RABBITMQ_HOST')
# RPC_PORT = os.environ.get('RABBITMQ_PORT', 5672)

# configurations for mongodb crawl status
# todo(): delete all MONGO* configs
# MONGO_RPC_DATABASE = os.environ.get('MONGO_RPC_DATABASE')
# MONGO_CRAWL_STATE_COLL = os.environ.get('MONGO_CRAWL_STATE_COLL')
# MONGO_RPC_USER = os.environ.get('MONGO_RPC_USER')
# MONGO_RPC_PASS = os.environ.get('MONGO_RPC_PASS')
# MONGODB_LOCATION = os.environ.get('MONGODB_LOCATION')

# prometheus configuration
PUSHGATEWAY_PORT = os.environ.get('PUSHGATEWAY_PORT')
PUSHGATEWAY_HOST = os.environ.get('PUSHGATEWAY_HOST')
PROMETHEUS_JOB = 'scrasync'


# HEXDIGEST FOR THE HASH

DIGEST_SIZE = 15
HEXDIGEST_SIZE = 30

