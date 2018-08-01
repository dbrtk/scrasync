
import asyncio

from .async_http import run
from .config import TEXT_C_TYPES
from .misc.validate_url import ValidateURL


def check_content_type(request):

    return request.content_type in TEXT_C_TYPES


class Scraper(object):

    def __init__(self, endpoint: list = None):

        self.endpoint_list = self.validated_urls(endpoint)
        self.loop = asyncio.get_event_loop()

    def __call__(self):

        self.filter_on_ctype()

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
            pass

    def filter_on_ctype(self):
        """ Filtering the list of urls, based on the content type. """

        self.endpoint_list = [
            _[2] for _ in self.head() if check_content_type(_[0])]

    def scrape(self):

        for web_page in self.get():
            pass


async def process_response(response, url):

    pass
