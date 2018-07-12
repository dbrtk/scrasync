

import asyncio

from aiohttp import (ClientConnectorError,
                     ClientConnectorSSLError, ClientSession, ClientSSLError)

from .config import DATA_FOLDER, HTTP_TIMEOUT
from .utils import get_random_user_agent


async def fetch(host, endpoint, session=None):
    """Returns the http response, the environment, the host."""
    try:
        async with session.get(
                endpoint, verify_ssl=False, timeout=HTTP_TIMEOUT) as response:
            return await response.read(), host
    except (ClientConnectorError, ClientConnectorSSLError,
            ClientSSLError, asyncio.TimeoutError) as err:
        return err, host


def get_user_agents():
    """Returns 10 random user agents."""
    return [get_random_user_agent() for _ in range(10)]


def client_session():
    """Returns a ClientSession for aiohttp."""
    agent_list = ['Mozilla/5.0', '(Macintosh; Intel Mac OS X 10_10_1)',
                  'AppleWebKit/537.36', '(KHTML, like Gecko)',
                  'Chrome/39.0.2171.95', 'Safari/537.36']
    return ClientSession(
        headers={'User-Agent': ' '.join(agent_list)}
    )


async def run(host_endpoint: list):

    tasks = []
    async with client_session() as session:
        for parameters in host_endpoint:
            task = asyncio.ensure_future(fetch(*parameters, session=session))
            tasks.append(task)
        return await asyncio.gather(*tasks)


if __name__ == "__main__":

    pass
