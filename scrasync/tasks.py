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
                   corpusid: str = None, corpus_file_path: str = None):
    """ Calling the html parser and saving the data to file. """

    if not os.path.isfile(path):
        return []

    with open(path, 'r') as html_txt:

        _dt = DataToTxt(url=endpoint, http_resp=html_txt.read())
        _dt()

    if not _dt:
        raise RuntimeError(_dt)

    links = _dt.links

    save_data.delay(**{
        'links': links,
        'corpus_file_path': corpus_file_path,
        'data': _dt.out_data,
        'title': _dt.title,
        'endpoint': endpoint,
        'corpus_id': corpusid
    })

    os.remove(path)
    if os.path.exists(path) and os.path.isfile(path):
        raise RuntimeError(path)

    return links


@celery.task(bind=True)
@save_task_id
def save_data(self, **kwds):
    """This task is saving a document on Proximity-bot -> DataModel and
       CorpusModel. This method will be called when scraping a page completes
       successfully.
    """
    celery.send_task(RMXBOT_TASKS.get('create_data'), kwargs=kwds)


@celery.task
def test_task(a, b):

    # todo(): delete

    return int(a) + int(b)


@celery.task
def crawl_ready(corpusid):
    """Check if the crawl is ready."""
    key = task_ids_key(corpusid)
    task_ids = list_lrange(key)
    out = {}
    count = 0
    for _id in task_ids:
        _id = str(_id)

        res = AsyncResult(_id, app=celery)
        is_ready = res.ready()

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
