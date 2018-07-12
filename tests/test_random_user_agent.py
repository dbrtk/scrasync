
from scrasync.async_http import get_user_agents
from scrasync.config import USER_AGENTS_FILE

from scrasync.utils import get_random_user_agent


def test_user_agent():

    out = get_random_user_agent()
    assert isinstance(out, str)


def test_against_agents_in_file():

    ua = get_random_user_agent()

    with open(USER_AGENTS_FILE, 'r') as _file:

        for _line in _file.readlines():
            if _line.strip() == ua.strip():
                break
        else:
            raise RuntimeError("`%s` does not exist in user agents list" % ua)


def test_user_agents_getter():

    assert len(get_user_agents()) == 10
