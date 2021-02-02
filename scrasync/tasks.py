import json
import os

import celery
from celery.result import AsyncResult

from .app import celery

# todo(): delete backend imports - depprecated
from .backend import list_lrange, list_lrem, task_ids_key

from .config.celeryconf import RMXBOT_TASKS
from . import crawl_state
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
    # set the ready state to true on the state object for this document.
    crawl_state.set_ready_state_true(containerid=corpusid, url=endpoint)

    if os.path.exists(path) and os.path.isfile(path):
        raise RuntimeError(path)
    return links


@celery.task
def test_task(a, b):

    # todo(): delete

    return int(a) + int(b)


@celery.task(bind=True)
def crawl_ready(self, containerid):

    #if crawl_state.list_ready_false(containerid=containerid):
        #return { 'ready': False }

    not_ready = []
    exceptions = []

    count = 0

    ready_tasks = []

    for taskobj in crawl_state.retrieve_taskids(containerid=containerid):

        res = AsyncResult(taskobj.get('taskid'), app=celery)

        is_ready = res.ready()
        if is_ready:
            ready_tasks.append(str(taskobj.get('_id')))
        else:
            not_ready.append(taskobj.get('taskid'))
            count += 1
        if res.failed() or not res.ready():

            exceptions.append({
                'ready': is_ready,
                'successful': res.successful(),
                'failed': res.failed(),
                'result': res.result,
                'status': res.status,
                'id': res.id
            })

    if ready_tasks:
        resp = crawl_state.remove_ready_tasks(docids=ready_tasks)

    if not_ready:
        return {
            'ready': False, 
            'tasks': not_ready,
            'count': count,
            'exceptions': exceptions 
        }
    crawl_state.prune_all(containerid=containerid)
    return { 'ready': True, 'exceptions': exceptions, 'count': count }


@celery.task(bind=True)
def crawl_ready_withredis(self, corpusid):
    """ Check if the crawl is ready.

        This funciton makes use of the backend module which needs an update.
    """
    # todo(): delete this - find another mechanism to do that.

    # todo(): delete!

    key = task_ids_key(corpusid)
    task_ids = list_lrange(key)
    out = {}
    count = 0
    
    pending_tasks = crawl_state.list_ready_false(containerid=str(corpusid))
    
    if pending_tasks:
        return { 'ready': False }
    tasks = crawl_state.state_list(containerid=str(corpusid))
    
    
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
