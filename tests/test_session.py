
import aiohttp

from scrasync.utils import get_random_user_agent


def test_session_user_agent():
    session = aiohttp.ClientSession()

    ua = get_random_user_agent()
    assert 1 + 1 == 2
