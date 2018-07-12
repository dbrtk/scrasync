

import os

from scrasync import config


def test_data_folder_exists():

    assert os.path.exists(config.DATA_FOLDER)


def test_data_folder():

    assert os.path.isdir(config.DATA_FOLDER)


def test_user_agents_file():

    assert os.path.exists(config.USER_AGENTS_FILE)
    assert os.path.isfile(config.USER_AGENTS_FILE)
