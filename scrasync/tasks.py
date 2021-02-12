""" Tasks for scrasync. """
import os

from .app import celery
from .config.celeryconf import RMXBOT_TASKS
from .data import DataToTxt
from .metrics import trackprogress


@celery.task(bind=True)
@trackprogress(dtype='parse_and_save')
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
