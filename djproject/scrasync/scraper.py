""" The scraper. """
import asyncio
import re

from djproject.app import celery
from djproject.celery_settings import SCRASYSNC_TASKS
from .async_http import run, run_with_tmp
from .config.appconf import CRAWL_MAX_PAGES, TEXT_C_TYPES
from . import crawl_state
from .misc.validate_url import ValidateURL
from .tasks import parse_and_save


def check_content_type(request):

    if request:
        return request.content_type in TEXT_C_TYPES
    return False


class Scraper:
    """ Scraping web pages using asyncio with aiohttp. """

    def __init__(self, endpoint: list = None, containerid: str = None, depth=1,
                 current_depth: int = 0, pages_count: int = 0,
                 target_path: str = None, crawlid: str = None):
        """ The initialisation of the scraper. """
        if not crawlid:
            raise RuntimeError('The crawlid is missing.')
        self.crawlid = crawlid
        self.endpoint_list = process_links(
            list(set(self.validated_urls(endpoint)))
        )
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

        self.containerid = containerid
        self.target_path = target_path

        self.max_depth = depth
        self.current_depth = current_depth
        self.pages_count = pages_count

    def __call__(self):

        self.endpoint_ditch_dupli()

        # self.filter_on_ctype()
        self.retrieve()

    def get_crawlid(self): return self.crawlid

    def endpoint_ditch_dupli(self):
        """ Getting rid of duplicated url(s). This method monitors endpoints
        sent to the scraper.
        """
        saved_endpoint = crawl_state.get_saved_endpoints(crawlid=self.crawlid)

        if saved_endpoint:
            self.endpoint_list = list(
                set(self.endpoint_list) - set(saved_endpoint))

        duplicates = crawl_state.push_many(
            containerid=self.containerid,
            urls=self.endpoint_list,
            crawlid=self.crawlid
        )
        self.endpoint_list = list(
            set(self.endpoint_list) - {i[0] for i in duplicates}
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
                'kwargs': {
                    'endpoint': url,
                    'path': tmp_path,
                    'containerid': self.containerid
                }
            }
            if self.current_depth < self.max_depth and \
               self.pages_count <= CRAWL_MAX_PAGES:

                parameters['link'] = crawl_links.s(
                    containerid=self.containerid,
                    crawlid=self.crawlid,
                    current_depth=self.current_depth,
                    pages_count=self.pages_count,
                    depth=self.max_depth
                )
            celery.send_task(SCRASYSNC_TASKS['parse_and_save'], **parameters)

    def filter_on_ctype(self):
        """ Filtering the list of urls, based on the content type. """

        self.endpoint_list = [
            _[2] for _ in self.head() if check_content_type(_[0])
        ]


@celery.task(bind=True)
def launch_crawl(self,
                 endpoint: str = None,
                 containerid: int = None,
                 depth: int = None,
                 **kwargs):
    """ This task launches the crawler; it is the parent task for other tasks
    that make the crawler. In this task a crawlid is created. The latter
    identifies the process for other tasks.
    """
    crawlid = crawl_state.make_crawlid(
        containerid=containerid,
        seed=endpoint
    )
    celery.send_task(SCRASYSNC_TASKS['start_crawl'], kwargs={
        'endpoint': endpoint,
        'crawlid': crawlid,
        'containerid': containerid,
        'depth': depth,
    })
    return crawlid


@celery.task(bind=True)
def start_crawl(self,
                endpoint: str = None,
                containerid: int = None,
                crawlid: str = None,
                depth: int = None,
                **kwargs):
    """ This task starts the crawler; it should be the parent task for others,
        that will follow.
    """
    if isinstance(endpoint, str):
        endpoint = [endpoint]
    Scraper(endpoint=endpoint,
            crawlid=crawlid,
            containerid=containerid,
            depth=depth,
            **kwargs)()


@celery.task(bind=True)
def crawl_links(self, links, **kwds):

    kwds['endpoint'] = links
    Scraper(**kwds)()


def process_links(links):
    """Given a list of url addresses, returns a list of unique urls with
    fragment identifeirs removed.
    """

    def cleanup(x):
        return re.sub(r'#.*$', '', x)

    return list(set(cleanup(item) if '#' in item else item
                    for item in links))
