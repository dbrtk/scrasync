
import hashlib

import redis

from scrasync.config.appconf import BROKER_HOST_NAME, REDIS_EXPIRATION_TIME

REDIS_DB = None


def redis_conn():

    global REDIS_DB

    if not isinstance(REDIS_DB, redis.client.Redis):

        REDIS_DB = redis.StrictRedis(
            host=BROKER_HOST_NAME,
            port=6379,
            db=0,
            charset="utf-8",
            decode_responses=True)

    return REDIS_DB


def scrape_get(*args, key: str = None):

    if args and not key:
        key = make_key(*args)

    return redis_conn().get(key)


def scrape_set_unique(*args, data: (list, str) = None):

    conn = redis_conn()
    key = make_key(*args)
    if conn.exists(key):
        return None
    conn.set(key, data)
    conn.expire(key, REDIS_EXPIRATION_TIME)
    return key


def scrape_set(*args, data: (list, str) = None, key: str = None):

    conn = redis_conn()
    if args and not key:
        key = make_key(*args)
    conn.set(key, data)
    conn.expire(key, REDIS_EXPIRATION_TIME)
    return key


def scrape_del(*args, key: str = None):

    if args and not key:
        key = make_key(*args)
    redis_conn().delete(key)


def make_key(*args):

    m = hashlib.blake2b(digest_size=64)
    for i in args:
        m.update(bytes(str(i), 'utf-8'))
    return m.hexdigest()


def key_exists(*args, key):

    if args and not key:
        key = make_key(*args)
    return redis_conn().exists(key)


def list_lpush(*args, key: str = None, value: str = None):

    if args and not key:
        key = make_key(*args)
    redis_conn().lpush(key, value)


def list_lrange(key, _from=0, _to=-1):
    """ Retrieves the entire list. """

    return redis_conn().lrange(key, _from, _to)


def list_lrem(key, value):
    """ Remove item from list. """

    return redis_conn().lrem(key, 0, value)


def task_ids_key(corpus_id):

    return '{}_{}'.format(corpus_id, 'taskids')
