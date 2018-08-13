import os

from celery import current_app, shared_task
from celery.result import AsyncResult

import requests

from .backend import scrape_del, scrape_get
from .data import DataToTxt
from .decorators import save_task_id


@shared_task(bind=True)
@save_task_id
def parse_html(self, endpoint: str = None, corpusid: str = None,
               corpus_file_path: str = None):

    http_resp = scrape_get(endpoint, corpusid)
    scrape_del(endpoint, corpusid)

    data = DataToTxt(url=endpoint, http_resp=http_resp)
    data()

    txt_list = data.out_data
    links = data.links

    save_data.delay(**{
        'links': links,
        'corpus_file_path': corpus_file_path,
        'data': txt_list,
        'title': data.title,
        'endpoint': endpoint,
        'corpus_id': corpusid
    })

    return links


@shared_task(bind=True)
@save_task_id
def parse_and_save(self, path: str = None, endpoint: str = None,
                   corpusid: str = None, corpus_file_path: str = None):
    """ Calling the html parser and saving the data to file. """

    if not os.path.isfile(path):
        return []

    with open(path, 'r', encoding='utf-8') as html_txt:

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

    requests.post('http://localhost:5000/data/create-data-object/',
                  json=kwds)


@shared_task(bind=True)
@save_task_id
def scrape_complete(self, **kwds):

    # todo(): implement
    pass
