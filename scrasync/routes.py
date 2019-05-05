
import asyncio

from celery.result import AsyncResult
from flask import Blueprint, jsonify

from .app import celery
from .backend import list_lrange, list_lrem, task_ids_key
from .tasks import test_task

scrasync_app = Blueprint('scrasync_app', __name__, root_path='/')


@scrasync_app.route('/')
def home():

    return jsonify({'success': True, 'text': 'Home page of scrasync'})


@scrasync_app.route('/test-celery/')
def test_celery():

    res = test_task.delay(1, 2).get()
    return jsonify({'success': True, 'result': res})


async def say(what, when):
    await asyncio.sleep(when)
    print('within asyncio say function')
    print(what)


@scrasync_app.route('/test-asyncio/')
def test_asyncio():

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(say('hello world', 1))
    loop.close()

    return jsonify({'success': True})


@scrasync_app.route('/crawl-ready/<objectid:corpusid>/')
def crawl_ready(corpusid):

    return jsonify(check_readiness(corpusid))


def check_readiness(corpusid):
    """Check f the crawl is ready."""
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
