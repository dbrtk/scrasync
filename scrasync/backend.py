
import hashlib

import redis

from .config import REDIS_DB_HOST, REDIS_EXPIRATION_TIME

REDIS_DB = redis.StrictRedis(host=REDIS_DB_HOST, port=6379, db=0)


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
