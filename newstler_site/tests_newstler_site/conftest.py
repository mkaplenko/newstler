import os
from unittest.mock import NonCallableMock

from yarl import URL

from newstler_site.external_services.news_storage import NewsStorage, NewsArticle

import django
from django.conf import settings
import pytest

# We manually designate which settings we will be using in an environment variable
# This is similar to what occurs in the `manage.py`
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newstler_site.django_facade.settings")


# `pytest` automatically calls this function once when tests are run.
def pytest_configure():
    settings.DEBUG = False
    # If you have any test specific settings, you can declare them here,
    # e.g.
    # settings.PASSWORD_HASHERS = (
    #     'django.contrib.auth.hashers.MD5PasswordHasher',
    # )
    django.setup()


def make_mock_news_storage():
    mock = NonCallableMock(NewsStorage)
    mock.get_news_by_user_data.return_value = [
        NewsArticle(id=777, title="Mock news", link=URL("www.tests.org"))
    ]
    return mock


@pytest.fixture(scope="session")
def news_storage():
    mock = make_mock_news_storage()
    return mock
