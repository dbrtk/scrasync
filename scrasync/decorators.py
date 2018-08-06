

from functools import wraps


from .backend import list_lpush, task_ids_key

import pprint
pp = pprint.PrettyPrinter(indent=4)


def save_task_id(func):
    """ this decorator saves the id of each task in the database; these are
    retrieved in order to check if all tasks accomplished and finished.

    all task should have a corpus id in the key-word parameters, this shoudl be
    called corpusid.

    """

    @wraps(func)
    def wrapped(self, *args, **kwds):

        corpusid = kwds.get('corpusid', None) or kwds.get('corpus_id', None)
        if not corpusid:
            raise RuntimeError(kwds)
        key = task_ids_key(corpusid)

        list_lpush(key=key, value=self.request.id)

        return func(self, *args, **kwds)

    return wrapped
