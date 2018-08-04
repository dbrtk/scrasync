""" simple image utils used across the app """

import random

from .config import USER_AGENTS_FILE


def random_line(afile):
    """Randomly chooses a line from a text file."""
    line = next(afile)
    for num, aline in enumerate(afile):
        if random.randrange(num + 2):
            continue
        line = aline
    return line


def get_random_user_agent():

    return random_line(open(USER_AGENTS_FILE, 'r')).strip()


def list_chunks(_list, n):

    for i in range(0, len(_list)):
        yield _list[i:i + n]


if __name__ == "__main__":
    print(get_random_user_agent())
