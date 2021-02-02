

from functools import wraps

import bson

from . import crawl_state


def save_task_id(func):
    """ This decorator saves the id of each task in the redis (or mongo) 
    database; task  ids are retrieved to check if all tasks completed and 
    finished.

    All task should have a container id in the key-word parameters, this should
    be called corpusid or containerid.
    """

    @wraps(func)
    def wrapped(self, *args, **kwds):

        containerid = kwds.get('corpusid', None) or kwds.get('corpus_id', None) \
            or kwds.get('containerid', None)
        if not containerid:
            raise RuntimeError(kwds)

        crawl_state.push_taskid(
            containerid=containerid, taskid=self.request.id)
        return func(self, *args, **kwds)

    return wrapped


def state_args(func):
    """ Converting args, kwds to the right data type. """

    @wraps(func)
    def wrapped(*args, **kwds):

        containerid = kwds.get('containerid', None)
        kwds['containerid'] = bson.ObjectId(containerid)

        return func(*args, **kwds)
    return wrapped
