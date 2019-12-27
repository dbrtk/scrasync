
import os

__HERE = os.path.abspath(__file__)


DATA_FOLDER = os.path.abspath(os.path.join(
    __HERE, os.pardir, os.pardir, os.pardir, 'data'))

USER_AGENTS_FILE = os.path.join(DATA_FOLDER, 'user-agents.txt')

PROXIMITY_USER = 'username'

HTTP_TIMEOUT = 10


# acceptable content_type
TEXT_C_TYPES = ['text/plain', 'text/html']


# the maximal amount of pages per crawl/corpus
CORPUS_MAX_PAGES = 500

# AIOHTTP CONFIG
AIOHTTP_MAX_URLS = 25


# REDIS CONFIG
# redis db host
REDIS_HOST_NAME = os.environ.get('REDIS_HOST_NAME')


# the expiration time is set to one hour.
REDIS_EXPIRATION_TIME = 60 * 60


# the size of the buffer for reading responses streamed by aiohttp.
AIOHTTP_BUFSIZE = 8 * 1024