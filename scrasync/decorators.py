""" The decorators for scrasync. """

from functools import wraps

import bson


def state_args(func):
    """ Converting args, kwds to the right data type. """

    @wraps(func)
    def wrapped(*args, **kwds):

        containerid = kwds.get('containerid', None)
        kwds['containerid'] = bson.ObjectId(containerid)

        return func(*args, **kwds)
    return wrapped
