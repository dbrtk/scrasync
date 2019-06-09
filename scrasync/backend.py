
import hashlib

import redis

from scrasync.config.appconf import REDIS_HOST_NAME, REDIS_EXPIRATION_TIME

REDIS_DB = redis.StrictRedis(
    host=REDIS_HOST_NAME, port=6379, db=0, charset="utf-8",
    decode_responses=True)


def scrape_get(*args, key: str = None):

    if args and not key:
        key = make_key(*args)

    return REDIS_DB.get(key)


def scrape_set_unique(*args, data: (list, str) = None):

    key = make_key(*args)
    if REDIS_DB.exists(key):
        return None
    REDIS_DB.set(key, data)
    REDIS_DB.expire(key, REDIS_EXPIRATION_TIME)
    return key


def scrape_set(*args, data: (list, str) = None, key: str = None):

    if args and not key:
        key = make_key(*args)
    REDIS_DB.set(key, data)
    REDIS_DB.expire(key, REDIS_EXPIRATION_TIME)
    return key


def scrape_del(*args, key: str = None):

    if args and not key:
        key = make_key(*args)
    REDIS_DB.delete(key)


def make_key(*args):

    m = hashlib.blake2b(digest_size=64)
    for i in args:
        m.update(bytes(str(i), 'utf-8'))
    return m.hexdigest()


def key_exists(*args, key):

    if args and not key:
        key = make_key(*args)
    return REDIS_DB.exists(key)


def list_lpush(*args, key: str = None, value: str = None):

    if args and not key:
        key = make_key(*args)
    REDIS_DB.lpush(key, value)


def list_lrange(key, _from=0, _to=-1):
    """ Retrieves the entire list. """

    return REDIS_DB.lrange(key, _from, _to)


def list_lrem(key, value):
    """ Remove item from list. """

    return REDIS_DB.lrem(key, 0, value)


def task_ids_key(corpus_id):

    return '{}_{}'.format(corpus_id, 'taskids')
