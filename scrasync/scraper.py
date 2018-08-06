
import asyncio
import json
import re

from celery import shared_task
from celery.contrib import rdb

from .async_http import run
from .backend import scrape_set, scrape_get
from .config import AIOHTTP_MAX_URLS, CORPUS_MAX_PAGES, TEXT_C_TYPES
from .decorators import save_task_id
from .misc.validate_url import ValidateURL
from .tasks import parse_html
from .utils import list_chunks

import pprint
pp = pprint.PrettyPrinter(indent=4)


def check_content_type(request):

    if request:
        return request.content_type in TEXT_C_TYPES
    return False


class Scraper(object):
    """ Scraping web pages using asyncio with aiohttp. """

    def __init__(self, endpoint: list = None, corpusid: str = None, depth=1,
                 current_depth: int = 0, pages_count: int = 0,
                 corpus_file_path: str = None):
        """ The initialisation of the scraper. """

        self.endpoint_list = process_links(
            list(set(self.validated_urls(endpoint)))
        )
        self.loop = asyncio.get_event_loop()

        self.corpusid = corpusid
        self.corpus_file_path = corpus_file_path

        self.max_depth = depth
        self.current_depth = current_depth
        self.pages_count = pages_count

    def __call__(self):

        self.endpoint_ditch_dupli()
        self.filter_on_ctype()
        self.retrieve_pages()

    def endpoint_ditch_dupli(self):
        """ Getting rid of duplicated url(s). This method monitors endpoints
        sent to the scraper.
        """
        key = '_'.join([self.corpusid, 'endpoint'])
        saved_endpoint = scrape_get(key=key)

        if saved_endpoint:
            saved_endpoint = json.loads(saved_endpoint)
            self.endpoint_list = list(
                set(self.endpoint_list) - set(saved_endpoint))
            scrape_set(key=key, data=json.dumps(
                self.endpoint_list + saved_endpoint))
        else:
            scrape_set(key=key, data=json.dumps(self.endpoint_list))

    def validated_urls(self, endpoint_list):

        return [_ for _ in endpoint_list if ValidateURL()(value=_)]

    def head(self):

        future = asyncio.ensure_future(run(self.endpoint_list, head_only=True))
        return self.loop.run_until_complete(future)

    def get(self):

        future = asyncio.ensure_future(run(self.endpoint_list))
        return self.loop.run_until_complete(future)

    def retrieve_pages(self):

        for resp, err, url in self.get():

            if err and not resp:
                continue

            scrape_set(url, self.corpusid, data=resp)
            del resp

            self.pages_count += 1
            self.current_depth += 1

            parameters = {
                'kwargs': {
                    'endpoint': url,
                    'corpusid': self.corpusid,
                    'corpus_file_path': self.corpus_file_path
                }
            }
            if self.current_depth < self.max_depth and \
               self.pages_count <= CORPUS_MAX_PAGES:
                parameters['link'] = scrape_links.s(
                    corpusid=self.corpusid,
                    corpus_file_path=self.corpus_file_path,
                    current_depth=self.current_depth,
                    pages_count=self.pages_count,
                    depth=self.max_depth
                )

            parse_html.apply_async(**parameters)

    def filter_on_ctype(self):
        """ Filtering the list of urls, based on the content type. """

        self.endpoint_list = [
            _[2] for _ in self.head() if check_content_type(_[0])]

    def scrape(self):

        for web_page in self.get():
            pass


@shared_task(bind=True)
@save_task_id
def scrape_links(self, links, **kwds):

    for items in list_chunks(links, AIOHTTP_MAX_URLS):
        kwds['endpoint'] = links
        call_the_scraper.delay(**kwds)


@shared_task(bind=True)
@save_task_id
def call_the_scraper(self, **kwds):

    Scraper(**kwds)()


def process_links(links):
    """Given a list of url addresses, returns a list of unique urls with
    fragment identifeirs removed.
    """

    def cleanup(x): return re.sub(r'#.*$', '', x)

    return list(set(cleanup(item) if '#' in item else item
                    for item in links))
