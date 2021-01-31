""" The module getting the database connection, the database and the collection.
"""
import enum
import hashlib

import bson
from pymongo import MongoClient

from .config.appconf import (
    MONGODB_LOCATION, MONGO_RPC_COLLECTION, MONGO_RPC_DATABASE, MONGO_RPC_PASS,
    MONGO_RPC_USER
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


def get_collection(collection: str = MONGO_RPC_COLLECTION):
    """ returns an instance of the mongodb collection """
    conn = get_connection(collection=collection)
    return conn[1]


class RecordType(enum.Enum):

    state = 'state'
    taskid = 'taskid'


class CrawlState:

    structure = {
        'crawlid': str,
        'containerid': bson.ObjectId,
        'url': str,
        'urlid': str,
        'ready': bool,
        '_type': str
    }
    def __init__(self, containerid, url, crawlid: str = None):

        self.crawlid = crawlid
        self.containerid = str(containerid)
        self.url = url
        self.urlid = make_key(url)
        self.ready = False
        self._type = RecordType.state.value

    def __call__(self):

        return {
            'crawlid': self.crawlid,
            'containerid': self.containerid,
            'url': self.url,
            'urlid': self.urlid,
            'ready': self.ready,
            '_type': self._type
        }


class TaskId:
    structure = {
        'containerid': str,
        'taskid': str,
        '_type': str
    }

    def __init__(self, containerid, taskid):

        self.containerid = containerid
        self.taskid = taskid
        self._type = RecordType.taskid.value

    def __call__(self):

        return {
            'containerid': self.containerid,
            '_type': self._type,
            'taskid': self.taskid
        }


#def del_state(*args, key: str = None):
    #""" Deleting the crawl state document from the database. """

    ## todo(): delete this
    #coll = get_collection()

    #if args and not key:
        #key = make_key(*args)
    #return coll.delete_many({'key': key})


def make_key(*args):
    """ Making a unique key that identifies the container's state. """
    hasher = hashlib.blake2b(digest_size=64)
    for i in args:
        hasher.update(bytes(str(i), 'utf-8'))
    return hasher.hexdigest()


def make_crawlid(containerid: str = None, seed: str = None):
    """ It calls the make_key function. The goal is to keep the ordering of
        arguments passed to make_key consistent.

        The 'seed' is the argument that contains the endpoint that starts the
        crawler - the seed.
    """
    return make_key(containerid, seed)


# below are functions that handle state per document/webpage being scraped

class DuplicateEndpointError(Exception):

    pass


#@state_args
#def state_push(containerid: str = None, url: str = None, check_dupli=False):
    #""" Create a document for a file/ webpage and push it to the state
        #collection.
    #"""

    ## todo(): delete
    #coll = get_collection()

    #state = CrawlState(containerid=containerid, url=url)()
    #if check_dupli:
        #if coll.find_one({
            #'containerid': containerid,
            #'url': url, 
            #'_type': RecordType.state.value
        #}):
            #raise DuplicateEndpointError(url)
    #return coll.insert_one(state)


@state_args
def push_many(containerid: str = None, urls: list = None):

    coll = get_collection()
    return coll.insert_many([
        CrawlState(containerid=containerid, url=url)() for url in urls
    ])


#@state_args
#def state_del(containerid: (str, bson.ObjectId) = None, url: str = None):
    #""" Delete a document from the state colleciton; this happend when the doc
        #has been saved to drive and the db.
    #"""

    ## todo(): delete
    #coll = get_collection()

    #return coll.remove({
        #'containerid': containerid,
        #'_type': RecordType.state.value,
        #'url': url
    #})


#@state_args
#def remove_from_state(containerid: (str, bson.ObjectId) = None):
    
    ## todo(): delete
    #coll = get_collection()
    #return coll.delete_many({
        #'containerid': containerid, 
        #'_type': RecordType.state.value
    #})


@state_args
def state_list(containerid: (str, bson.ObjectId) = None):
    """ For a containerid, retrieve all documents. This shows all active 
        processes (scraping, html cleanup, writng to disk).
    """
    coll = get_collection()

    return coll.find({
        'containerid': containerid,
        '_type': RecordType.state.value
    })


@state_args
def list_ready_false(containerid: str = None):

    coll = get_collection()
    return coll.find({
        'containerid': containerid, 
        'ready': False,
        '_type': RecordType.state.value
    })


@state_args
def list_ready_true(containerid: str = None):

    coll = get_collection()
    return coll.find({
        'containerid': containerid, 
        'ready': True,
        '_type': RecordType.state.value
    })


@state_args
def set_ready_state_true(containerid: str = None, url: str = None):

    coll = get_collection()
    return coll.update_many({
            'containerid': containerid, 
            'url': url
        },
        {'$set': { 'ready': True }
    })


#@state_args
#def find_dupli(containerid: str = None, url: str = None):
    
    ## todo(): delete
    #coll = get_collection()

    #return coll.find_one({
        #'containerid': containerid,
        #'_type': RecordType.state.value,
        #'url': url
    #})


def get_saved_endpoints(containerid: (str, bson.ObjectId) = None):
    """ Returns alist of saved endpoints. """
    return [_.get('url') for item in 
            state_list(containerid=containerid)]





# todo(): delete all the functions below

@state_args
def push_taskid(containerid: (str, bson.ObjectId) = None, taskid: str = None):

    coll = get_collection()
    return coll.insert_one(TaskId(containerid=containerid, taskid=taskid)())


@state_args
def retrieve_taskids(containerid: (str, bson.ObjectId) = None):

    coll = get_collection()
    return coll.find({
        '_type': RecordType.taskid.value,
        'containerid': containerid
    })


def get_taskids(containerid: (str, bson.ObjectId) = None):

    return (_.get('taskid') for _ in 
            retrieve_taskids(containerid=containerid))


@state_args
def prune_taskids(containerid: (str, bson.ObjectId) = None):

    coll = get_collection()
    return coll.remove({
        '_type': RecordType.taskid.value,
        'containerid': containerid
    })


@state_args
def prune_all(containerid: (str, bson.ObjectId) = None):
    
    coll = get_collection()
    return coll.remove({'containerid': containerid})


def remove_ready_tasks(docids: list = None):
    """ remove records for tasks that succeded """
    coll = get_collection()
    return coll.delete_many({'_id': {'$in': docids}})

