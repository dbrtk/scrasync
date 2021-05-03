""" The module getting the database connection, the database and the collection.
"""
import datetime
import hashlib

# import bson
# from pymongo import MongoClient

from .app import celery

# from .config.appconf import (
#     MONGO_CRAWL_STATE_COLL, MONGODB_LOCATION, MONGO_RPC_DATABASE,
#     MONGO_RPC_PASS, MONGO_RPC_USER
# )
from .config.celeryconf import RMXWEB_TASKS, RMXWEB_QUEUE_NAME


CLIENT = None


# def get_client():
#     # todo(): delete!
#     global CLIENT
#     if not isinstance(CLIENT, MongoClient):
#         CLIENT = MongoClient(MONGODB_LOCATION,
#                              username=MONGO_RPC_USER,
#                              password=MONGO_RPC_PASS,
#                              authSource=MONGO_RPC_DATABASE)
#     return CLIENT


# def get_connection(db: str = MONGO_RPC_DATABASE, collection: str = None):
#     """ returns a database connection and the collection """
#     # todo(): delete!
#     assert isinstance(collection, str), "No collection name provided."
#     cli = get_client()
#     database = cli[db]
#     collection = database[collection]
#     return database, collection


# def get_collection(collection: str = None):
#     """ returns an instance of the mongodb collection """
#     # todo(): delete!
#     conn = get_connection(collection=collection)
#     return conn[1]


# class CrawlState:
#     # todo(): delete this class.
#     structure = {
#         'crawlid': str,
#         'containerid': int,
#         'url': str,
#         'urlid': str,
#         'ready': bool,
#         'created': datetime.datetime
#     }
#
#     def __init__(self, containerid, url, crawlid: str = None):
#
#         self.crawlid = crawlid
#         self.containerid = int(containerid)
#         self.url = url
#         self.urlid = make_key(url)
#         self.ready = False
#         self.created = datetime.datetime.now()
#
#     def __call__(self):
#
#         return {
#             'crawlid': self.crawlid,
#             'containerid': self.containerid,
#             'url': self.url,
#             'urlid': self.urlid,
#             'ready': self.ready,
#             'created': self.created
#         }


def make_key(*args):
    """ Making a unique key that identifies the container's state. """
    hasher = hashlib.blake2b(digest_size=64)
    for i in args:
        hasher.update(bytes(str(i), 'utf-8'))
    return hasher.hexdigest()


def make_crawlid(containerid: int = None, seed: (list, str) = None):
    """ It calls the make_key function. The goal is to keep the ordering of
        arguments passed to make_key consistent.

        The 'seed' is the argument that contains the endpoint that starts the
        crawler - the seed.
    """
    seed = seed if isinstance(seed, list) else [seed]
    return make_key(containerid, *seed)


# below are functions that handle state per document/webpage being scraped

def push_many(containerid: int = None, urls: list = None, crawlid: str = None):
    """ Push many items to the crawl_state collection.
    Urls are contained in a list of tuples with a url and a urlid:
    (url, urlid).
    """
    urls = [(url, make_key(url)) for url in urls]
    return celery.send_task(RMXWEB_TASKS['push_many'], kwargs={
        'containerid': containerid,
        'urls': urls,
        'crawlid': crawlid
    }).get()


# def state_list(crawlid: str = None, containerid: int = None):
#     """ For a containerid, retrieve all documents. This shows all active
#         processes (scraping, html cleanup, writng to disk).
#     """
#     # todo(): delete this function
#     coll = get_collection(collection=MONGO_CRAWL_STATE_COLL)
#
#     if containerid:
#         return coll.find({'containerid': containerid})
#     return coll.find({'crawlid': crawlid})


def get_saved_endpoints(containerid: int = None):
    """ Returns alist of saved endpoints. """
    return celery.send_task(RMXWEB_TASKS['get_saved_endpoints'], kwargs={
        'containerid': containerid
    }).get()
    # return [_.get('url') for _ in state_list(containerid=containerid)]


#
# def push_many(containerid: int = None, urls: list = None, crawlid: str = None):
#     """ Push many items to the crawl_state collection. """
#     coll = get_collection(collection=MONGO_CRAWL_STATE_COLL)
#
#     return coll.insert_many([
#         CrawlState(containerid=containerid, url=url, crawlid=crawlid)()
#         for url in urls
#     ], ordered=False)
#
#
# def state_list(crawlid: str = None, containerid: int = None):
#     """ For a containerid, retrieve all documents. This shows all active
#         processes (scraping, html cleanup, writng to disk).
#     """
#     coll = get_collection(collection=MONGO_CRAWL_STATE_COLL)
#
#     if containerid:
#         return coll.find({'containerid': containerid})
#     return coll.find({'crawlid': crawlid})
#
#
# def get_saved_endpoints(containerid: int = None):
#     """ Returns alist of saved endpoints. """
#     return [_.get('url') for _ in state_list(containerid=containerid)]
