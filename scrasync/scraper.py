
import asyncio
import json
import re
import uuid

from .app import celery
from .async_http import run, run_with_tmp
import pymongo

from .config.appconf import CRAWL_MAX_PAGES, TEXT_C_TYPES
from .config.celeryconf import SCRASYNC_TASKS
from . import crawl_state
from .decorators import save_task_id
from .misc.validate_url import ValidateURL
from .tasks import parse_and_save


def check_content_type(request):

    if request:
        return request.content_type in TEXT_C_TYPES
    return False


class Scraper(object):
    """ Scraping web pages using asyncio with aiohttp. """

    def __init__(self, endpoint: list = None, corpusid: str = None, depth=1,
                 current_depth: int = 0, pages_count: int = 0,
                 target_path: str = None, crawlid: str = None,
                 queue: str = None):
        """ The initialisation of the scraper. """

        self.crawlid = crawlid if crawlid \
            else crawl_state.make_crawlid(
                containerid=corpusid,
                seed=endpoint
            )
        if not queue:
            raise RuntimeError('The queue name is missing.')
        self.queue = queue
        self.endpoint_list = process_links(
            list(set(self.validated_urls(endpoint)))
        )
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

        self.corpusid = corpusid
        self.target_path = target_path

        self.max_depth = depth
        self.current_depth = current_depth
        self.pages_count = pages_count

    def __call__(self):

        self.endpoint_ditch_dupli()

        # self.filter_on_ctype()
        self.retrieve()

    def endpoint_ditch_dupli(self):
        """ Getting rid of duplicated url(s). This method monitors endpoints
        sent to the scraper.
        """
        saved_endpoint = crawl_state.get_saved_endpoints(self.corpusid)

        if saved_endpoint:
            self.endpoint_list = list(
                set(self.endpoint_list) - set(saved_endpoint))
        try:
            resp = crawl_state.push_many(
                containerid=self.corpusid,
                urls=self.endpoint_list,
                crawlid=self.crawlid
            )
        except pymongo.errors.BulkWriteError as err:

            dupli_urls = [_.get('keyValue').get('url')
                          for _ in err.details['writeErrors']]
            self.endpoint_list = list(
                set(self.endpoint_list) - set(dupli_urls)
            )

    def validated_urls(self, endpoint_list):
        """ Validating urls. """
        return [_ for _ in endpoint_list if ValidateURL()(value=_)]

    def head(self):
        """ For a list of endpoints, retrieves the headers. """
        future = asyncio.ensure_future(run(self.endpoint_list, head_only=True))
        return self.loop.run_until_complete(future)

    def get(self):
        """ For a list of endpoints (self.endpoint_list), retrieves the content,
        making http (get) queries.
        """
        # future = asyncio.ensure_future(run(self.endpoint_list))
        future = asyncio.ensure_future(run_with_tmp(self.endpoint_list))
        return self.loop.run_until_complete(future)

    def retrieve(self):
        """ Retrieving pages using the responses saved to tempfiles. """
        self.current_depth += 1

        for tmp_path, err, url in self.get():

            if not tmp_path or err:
                continue

            self.pages_count += 1

            parameters = {
                'queue': self.queue,
                'kwargs': {
                    'endpoint': url,
                    'path': tmp_path,
                    'corpusid': self.corpusid
                }
            }

            if self.current_depth < self.max_depth and \
               self.pages_count <= CRAWL_MAX_PAGES:

                parameters['link'] = crawl_links.s(
                    corpusid=self.corpusid,
                    crawlid=self.crawlid,
                    current_depth=self.current_depth,
                    pages_count=self.pages_count,
                    depth=self.max_depth
                )
            celery.send_task(
                SCRASYNC_TASKS['parse_and_save'], **parameters
            )
            # parse_and_save.apply_async(**parameters)

    def filter_on_ctype(self):
        """ Filtering the list of urls, based on the content type. """

        self.endpoint_list = [
            _[2] for _ in self.head() if check_content_type(_[0])]


def queue_name(): return f'scrasync.{uuid.uuid4().hex}'


@celery.task(bind=True)
@save_task_id
def start_crawl(self, **kwds):
    """ This task starts the crawler; it should be the parent task for others,
        that will follow.
    """
    queue = queue_name()

    celery.control.add_consumer(queue, reply=True)
    kwds['queue'] = queue
    params = { 'queue': queue, 'kwargs': kwds }

    celery.send_task(SCRASYNC_TASKS['instantiate_scraper'], **params)
    return { 'queue': queue }


@celery.task(bind=True)
@save_task_id
def instantiate_scraper(self, **kwds):
    """
    """
    print(f'\nInside the instantiate_scraper function.', flush=True)
    print(f'\nkwargs: {kwds}', flush=True)
    endpoint = kwds.get('endpoint')

    if isinstance(endpoint, str):
        kwds['endpoint'] = [endpoint]

    Scraper(**kwds)()


@celery.task(bind=True)
@save_task_id
def crawl_links(self, links, **kwds):

    kwds['endpoint'] = links
    Scraper(**kwds)()


def process_links(links):
    """Given a list of url addresses, returns a list of unique urls with
    fragment identifeirs removed.
    """

    def cleanup(x): return re.sub(r'#.*$', '', x)

    return list(set(cleanup(item) if '#' in item else item
                    for item in links))
