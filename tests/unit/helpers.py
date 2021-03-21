import os

import pytest

TMP_DIR = os.path.join(os.path.dirname(__file__), 'local-compose-tmp-dir-test')
TMP_DIR_BIN = os.path.join(TMP_DIR, 'bin')


@pytest.fixture
def set_current_dir_fixture():
    real_cwd = os.getcwd()
    os.makedirs(TMP_DIR_BIN)
    os.chdir(TMP_DIR)
    yield
    os.rmdir(TMP_DIR_BIN)
    os.rmdir(TMP_DIR)
    os.chdir(real_cwd)
