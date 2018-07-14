

import asyncio

from aiohttp import (ClientConnectorError,
                     ClientConnectorSSLError, ClientSession, ClientSSLError)

from .config import HTTP_TIMEOUT
from .utils import get_random_user_agent


TEXT_C_TYPES = ['text/plain', 'text/html']


class Error(Exception):
    pass


class ContentTypeError(Error):

    msg = 'Wrong content type.'

    def __init__(self, message):
        self.message = "%s %s" % (self.msg, message)


async def fetch(endpoint, session=None):
    """Returns the http response, the environment."""
    try:
        async with session.get(
                endpoint, verify_ssl=False, timeout=HTTP_TIMEOUT) as response:
            content_type = response.content_type
            if content_type in TEXT_C_TYPES:
                return await response.read(), endpoint
            else:
                del response
                raise ContentTypeError(message=content_type)
    except (ClientConnectorError, ClientConnectorSSLError,
            ClientSSLError, asyncio.TimeoutError, ContentTypeError) as err:
        return err, endpoint


async def fetch_head(endpoint, session: ClientSession = None):
    """ Querying the endpoint for the headers. """
    try:
        async with session.head(endpoint) as response:
            return response, endpoint
    except (asyncio.TimeoutError, ClientConnectorError) as err:
        return err, endpoint


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


if __name__ == "__main__":

    pass
