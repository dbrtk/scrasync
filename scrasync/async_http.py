
import asyncio
import tempfile

from aiohttp import (ClientConnectorError, ClientConnectorSSLError,
                     ClientSession, ClientSSLError, ClientTimeout)
from aiohttp.client_exceptions import ClientConnectionError

from .config import AIOHTTP_BUFSIZE, HTTP_TIMEOUT, TEXT_C_TYPES
from .utils import get_random_user_agent


class Error(Exception):
    pass


class ContentTypeError(Error):

    msg = 'Wrong content type.'

    def __init__(self, message):
        self.message = "%s %s" % (self.msg, message)


TIMEOUT = ClientTimeout(total=HTTP_TIMEOUT)

ERRORS = (ClientConnectionError, ClientConnectorError, ClientConnectorSSLError,
          ClientSSLError, asyncio.TimeoutError, ConnectionResetError,
          ConnectionError, ContentTypeError, UnicodeDecodeError)


async def fetch_chunks_totmp(endpoint, session=None):

    try:
        async with session.get(
                endpoint, verify_ssl=False, timeout=TIMEOUT) as response:
            if response.content_type not in TEXT_C_TYPES:
                del response
                return None, None, endpoint

            file_name = None
            encoding = 'utf-8'  # response.get_encoding()

            with tempfile.NamedTemporaryFile(delete=False, mode='w+') as tmpf:
                file_name = tmpf.name
                while True:
                    chunk = await response.content.read(AIOHTTP_BUFSIZE)
                    if not chunk:
                        break
                    tmpf.write(chunk.decode(
                        encoding=encoding, errors='strict'))
        return file_name, None, endpoint
    except ERRORS as err:
        return None, err, endpoint


async def fetch_totmp(endpoint, session=None):

    try:
        async with session.get(
                endpoint, verify_ssl=False, timeout=TIMEOUT) as response:
            if response.content_type not in TEXT_C_TYPES:
                del response
                return None, None, endpoint

            file_name = None

            with tempfile.NamedTemporaryFile(delete=False, mode='w+') as tmpf:
                file_name = tmpf.name

                txt = await response.text()
                # encoding = response.get_encoding()

                tmpf.write(txt)

        return file_name, None, endpoint
    except ERRORS as err:
        return None, err, endpoint


async def fetch(endpoint, session=None):
    """Returns the http response, the environment."""
    try:
        async with session.get(
                endpoint, verify_ssl=False, timeout=TIMEOUT) as response:

            if response.content_type not in TEXT_C_TYPES:
                del response
                return None, None, endpoint

            return await response.text(encoding="utf-8"), None, endpoint

    except ERRORS as err:
        return None, err, endpoint


async def fetch_head(endpoint, session: ClientSession = None):
    """ Querying the endpoint for the headers. """
    try:
        async with session.head(endpoint) as response:
            return response, None, endpoint
    except (asyncio.TimeoutError, ClientConnectorError) as err:
        return None, err, endpoint


def get_user_agents():
    """Returns 10 random user agents.
       This will be useful for rotating user agents.
    """
    return [get_random_user_agent() for _ in range(10)]


def client_session():
    """Returns a ClientSession for aiohttp."""
    return ClientSession(
        headers={'User-Agent': get_random_user_agent()}
    )


async def run(endpoint_list: list, head_only: bool = False):
    tasks = []
    async with client_session() as session:
        for endpoint in endpoint_list:
            if head_only:
                task = asyncio.ensure_future(
                    fetch_head(endpoint, session=session))
            else:
                task = asyncio.ensure_future(fetch(endpoint, session=session))
            tasks.append(task)
        return await asyncio.gather(*tasks)


async def run_with_tmp(endpoint: list = None):

    tasks = []
    async with client_session() as session:
        for _ in endpoint:
            tasks.append(asyncio.ensure_future(
                fetch_totmp(_, session=session)))
        return await asyncio.gather(*tasks)


if __name__ == "__main__":

    pass
