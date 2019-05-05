

import os

from scrasync.config import appconf


def test_data_folder_exists():

    assert os.path.exists(appconf.DATA_FOLDER)


def test_data_folder():

    assert os.path.isdir(appconf.DATA_FOLDER)


def test_user_agents_file():

    assert os.path.exists(appconf.USER_AGENTS_FILE)
    assert os.path.isfile(appconf.USER_AGENTS_FILE)
