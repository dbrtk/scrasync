import os

from celery import shared_task
import requests

from .config import CREATE_DATA_ENDPOINT
from .data import DataToTxt
from .decorators import save_task_id


@shared_task(bind=True)
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


@shared_task(bind=True)
@save_task_id
def save_data(self, **kwds):
    """This task is saving a document on Proximity-bot -> DataModel and
       CorpusModel. This method will be called when scraping a page completes
       successfully.
    """
    requests.post(CREATE_DATA_ENDPOINT, json=kwds)


@shared_task
def test_task(a, b):
    return a + b
