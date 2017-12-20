"""Module contains base types and implement specific classes for news storage"""
from abc import ABC, abstractmethod
from collections import namedtuple
from enum import Enum
from typing import Iterable

from django_app.models import NewsItem
from newstler_site.external_services.linkedin_client import UserData


class Tag(Enum):
    PYTHON = "python"
    JS = "javascript"


NewsArticle = namedtuple("NewItem", ("id", "title", "link"))


class NewsStorage(ABC):
    @abstractmethod
    def get_news_by_user_data(self, user_data: UserData) -> Iterable[NewsArticle]:
        """Get sequence of news according given experience"""


class FakeNewsStorage(NewsStorage):
    def get_news_by_user_data(self, user_data: UserData) -> Iterable[NewsArticle]:
        return [NewsArticle(id=0, title="Python", link="http://www.fake.ru")]


class DjangoORMBasedStorage(NewsStorage):
    def get_news_by_user_data(self, user_data: UserData) -> Iterable[NewsArticle]:
        tags = (tag.value for tag in Tag if tag.value in user_data.position.lower())
        news = NewsItem.objects.all() if not tags else NewsItem.objects.filter(tag__name__in=tags)

        return (NewsArticle(id=x.pk, title=x.title, link=x.link) for x in news)
