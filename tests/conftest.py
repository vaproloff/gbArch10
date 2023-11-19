import os
import pytest
from sqlalchemy_utils import create_database, drop_database

os.environ['TESTING'] = 'True'

from db import TEST_SQLALCHEMY_DATABASE_URL


@pytest.fixture(scope="module")
def temp_db():
    create_database(TEST_SQLALCHEMY_DATABASE_URL)

    try:
        yield TEST_SQLALCHEMY_DATABASE_URL
    finally:
        drop_database(TEST_SQLALCHEMY_DATABASE_URL)
