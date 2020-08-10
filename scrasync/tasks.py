
import os

from celery.result import AsyncResult

from .app import celery
from .backend import list_lrange, list_lrem, task_ids_key
from .config.celeryconf import RMXBOT_TASKS
from .data import DataToTxt
from .decorators import save_task_id


@celery.task(bind=True)
@save_task_id
def parse_and_save(self, path: str = None, endpoint: str = None,
                   corpusid: str = None):
    """ Calling the html parser and saving the data to file. """

    if not os.path.isfile(path):
        return []

    with open(path, 'r') as html_txt:
        _dt = DataToTxt(url=endpoint, http_resp=html_txt.read())
        _dt()

    if not _dt:
        raise RuntimeError(_dt)
    links = _dt.links

    celery.send_task(RMXBOT_TASKS.get('create_data'), kwargs={
        'corpusid': corpusid,
        'endpoint': endpoint,
        'title': _dt.title,
        'data': _dt.out_data,
        'links': links,
    })

    os.remove(path)
    if os.path.exists(path) and os.path.isfile(path):
        raise RuntimeError(path)
    return links


@celery.task
def test_task(a, b):

    # todo(): delete

    return int(a) + int(b)


@celery.task(bind=True)
def crawl_ready(self, corpusid):
    """Check if the crawl is ready."""
    key = task_ids_key(corpusid)
    task_ids = list_lrange(key)
    out = {}
    count = 0

    for _id in task_ids:
        _id = str(_id)

        res = AsyncResult(_id, app=celery)
        is_ready = res.ready()

        # todo(): retry PENDING tasks
        # todo(): set max_retry to 3

        if is_ready:
            list_lrem(key, _id)
        else:
            out[_id] = is_ready
            count += 1
    if out:
        return {'ready': False, 'tasks': out, 'count': count}
    else:
        # todo(): remove the list from redis
        pass

    return {'ready': True}
