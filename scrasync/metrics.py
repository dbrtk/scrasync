

from functools import wraps
import time
import uuid

import prometheus_client as promc

from .config.appconf import PROMETHEUS_JOB, PUSHGATEWAY_HOST, PUSHGATEWAY_PORT

# registry = promc.CollectorRegistry()

START_PROG_PREFIX = 'start_crawl'
CRAWL_PROG_PREFIX = 'crawl_links'
PARSE_PROG_PREFIX = 'parse_and_save'

LAST_CALL = 'lastcall'


def make_progress_name(dtype: str = None, containerid: str = None): 

    # return f'{dtype}_{containerid}_{uuid.uuid4().hex}'
    return f'{dtype}_{containerid}'


def make_lastcall_name(dtype: str = None, containerid: str = None):

    return f'{dtype}_{containerid}_{LAST_CALL}'


def trackprogress(dtype: str = None):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwds):

            assert dtype in [START_PROG_PREFIX, CRAWL_PROG_PREFIX,
                             PARSE_PROG_PREFIX]
            registry = promc.CollectorRegistry()
            containerid = kwds.get('containerid') or kwds.get('corpusid')
            prog_name = make_progress_name(dtype, containerid)
            g = promc.Gauge(
                prog_name, f'the progress of {dtype}', registry=registry
            )
            last = promc.Gauge(
                make_lastcall_name(dtype, containerid),
                f'the time in seconds of last call made to {dtype}',
                registry=registry
            )
            print(f'inside the wrapper. containerid: {containerid}', flush=True)
            try:
                with g.time():
                    out = func(*args, **kwds)

            except Exception as err:
                out = None
            finally:
                last.set(time.time())
                promc.pushadd_to_gateway(
                    f'{PUSHGATEWAY_HOST}:{PUSHGATEWAY_PORT}',
                    job=PROMETHEUS_JOB,
                    registry=registry
                )
            return out
        return wrapper
    return inner

