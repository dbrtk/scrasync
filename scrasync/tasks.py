

from celery import shared_task
import requests

from .backend import scrape_del, scrape_get  # , scrape_set
from .data import DataToTxt


@shared_task(bind=True)
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


@shared_task
def save_data(**kwds):

    requests.post('http://localhost:5000/data/create-data-object/',
                  json=kwds)
