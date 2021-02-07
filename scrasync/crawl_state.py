""" The module getting the database connection, the database and the collection.
"""
import datetime
import enum
import hashlib

import bson
from pymongo import MongoClient

from .config.appconf import (
    MONGO_CRAWL_RESULTS_COLL, MONGO_CRAWL_STATE_COLL, MONGODB_LOCATION,
    MONGO_RPC_DATABASE, MONGO_RPC_PASS, MONGO_RPC_USER
)
from .decorators import state_args


CLIENT = None


def get_client():

    global CLIENT
    if not isinstance(CLIENT, MongoClient):
        CLIENT = MongoClient(MONGODB_LOCATION,
                             username=MONGO_RPC_USER,
                             password=MONGO_RPC_PASS,
                             authSource=MONGO_RPC_DATABASE)
    return CLIENT


def get_connection(db: str = MONGO_RPC_DATABASE, collection: str = None):
    """ returns a database connection and the collection """
    assert isinstance(collection, str), "No collection name provided."
    cli = get_client()
    database = cli[db]
    collection = database[collection]
    return database, collection


def get_collection(collection: str = None):
    """ returns an instance of the mongodb collection """
    conn = get_connection(collection=collection)
    return conn[1]


class CrawlState:

    structure = {
        'crawlid': str,
        'containerid': bson.ObjectId,
        'url': str,
        'urlid': str,
        'ready': bool,
        'created': datetime.datetime
    }
    def __init__(self, containerid, url, crawlid: str = None):

        self.crawlid = crawlid
        self.containerid = bson.ObjectId(containerid)
        self.url = url
        self.urlid = make_key(url)
        self.ready = False
        self.created = datetime.datetime.now()

    def __call__(self):

        return {
            'crawlid': self.crawlid,
            'containerid': self.containerid,
            'url': self.url,
            'urlid': self.urlid,
            'ready': self.ready,
            'created': self.created
        }


class TaskId:
    structure = {
        'containerid': str,
        'taskid': str,
        'created': datetime.datetime
    }

    def __init__(self, containerid, taskid):

        self.containerid = containerid
        self.taskid = taskid
        self.created = datetime.datetime.now()

    def __call__(self):

        return {
            'containerid': self.containerid,
            'taskid': self.taskid,
            'created': self.created
        }


def make_key(*args):
    """ Making a unique key that identifies the container's state. """
    hasher = hashlib.blake2b(digest_size=64)
    for i in args:
        hasher.update(bytes(str(i), 'utf-8'))
    return hasher.hexdigest()


def make_crawlid(containerid: str = None, seed: (list, str) = None):
    """ It calls the make_key function. The goal is to keep the ordering of
        arguments passed to make_key consistent.

        The 'seed' is the argument that contains the endpoint that starts the
        crawler - the seed.
    """
    seed = seed if isinstance(seed, list) else [seed]
    return make_key(containerid, *seed)


# below are functions that handle state per document/webpage being scraped


@state_args
def push_many(containerid: str = None, urls: list = None, crawlid: str = None):
    """ Push many items to the crawl_state collection. """
    coll = get_collection(collection=MONGO_CRAWL_STATE_COLL)

    return coll.insert_many([
        CrawlState(containerid=containerid, url=url, crawlid=crawlid)()
        for url in urls
    ], ordered=False)


@state_args
def state_list(crawlid: str = None, containerid: str = None):
    """ For a containerid, retrieve all documents. This shows all active 
        processes (scraping, html cleanup, writng to disk).
    """
    coll = get_collection(collection=MONGO_CRAWL_STATE_COLL)

    if containerid:
        return coll.find({'containerid': containerid})
    return coll.find({'crawlid': crawlid})


@state_args
def list_ready_false(containerid: str = None):

    coll = get_collection(collection=MONGO_CRAWL_STATE_COLL)
    return coll.find({
        'containerid': containerid, 
        'ready': False
    })


@state_args
def list_ready_true(containerid: str = None):

    coll = get_collection(collection=MONGO_CRAWL_STATE_COLL)
    return coll.find({
        'containerid': containerid, 
        'ready': True,
    })


@state_args
def set_ready_state_true(containerid: str = None, url: str = None):

    coll = get_collection(collection=MONGO_CRAWL_STATE_COLL)
    return coll.update_many({
            'containerid': containerid, 
            'url': url
        },
        {'$set': { 'ready': True }
    })


def get_saved_endpoints(containerid: (str, bson.ObjectId) = None):
    """ Returns alist of saved endpoints. """
    return [_.get('url') for _ in state_list(containerid=containerid)]



# CELERY'S TASKIDS SAVED IN THE MONGO DATABASE --> STATUS CHECK
# these are related to the monitoring of celery tasks with AsyncResult.
# once this functionality is migrated to prometheus, they won't be needed.

@state_args
def push_taskid(containerid: (str, bson.ObjectId) = None, taskid: str = None):

    coll = get_collection(collection=MONGO_CRAWL_RESULTS_COLL)
    return coll.insert_one(TaskId(containerid=containerid, taskid=taskid)())


@state_args
def retrieve_taskids(containerid: (str, bson.ObjectId) = None):

    coll = get_collection(collection=MONGO_CRAWL_RESULTS_COLL)
    return coll.find({
        'containerid': containerid
    })


def get_taskids(containerid: (str, bson.ObjectId) = None):

    return (_.get('taskid') for _ in 
            retrieve_taskids(containerid=containerid))


@state_args
def prune_taskids(containerid: (str, bson.ObjectId) = None):

    coll = get_collection(collection=MONGO_CRAWL_RESULTS_COLL)
    return coll.remove({
        'containerid': containerid
    })


@state_args
def prune_all(containerid: (str, bson.ObjectId) = None):
    
    coll = get_collection(collection=MONGO_CRAWL_RESULTS_COLL)
    return coll.remove({'containerid': containerid})


def remove_ready_tasks(docids: list = None):
    """ remove records for tasks that succeded """
    coll = get_collection(collection=MONGO_CRAWL_RESULTS_COLL)
    docids = docids if all(isinstance(_, bson.ObjectId) for _ in docids) else \
        [bson.ObjectId(_) for _ in docids]
    return coll.delete_many({'_id': {'$in': docids}})
