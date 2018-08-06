

from celery.result import AsyncResult
from django.http import JsonResponse

from ..backend import list_lrange, list_lrem, task_ids_key


def create(request):

    pass


def crawl_ready(request, corpusid):
    return JsonResponse(check_readiness(corpusid))


def check_readiness(corpusid):
    key = task_ids_key(corpusid)
    task_ids = list_lrange(key)
    out = {}
    count = 0
    for _id in task_ids:
        _id = str(_id)

        res = AsyncResult(_id)
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
