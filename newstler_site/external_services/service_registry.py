"""Classes that implement service-discovery mechanism."""
from abc import ABC, abstractmethod
from configparser import ConfigParser
import logging

from newstler_site.external_services.linkedin_client import LinkedInClient, FakeLinkedInClient, RestLinkedInClient
from newstler_site.config import options

from cached_property import cached_property

from newstler_site.external_services.news_storage import NewsStorage, DjangoORMBasedStorage


LOG = logging.getLogger('consolelogger')


class ServiceRegistry(ABC):
    """
    Registry for all external services. First configure it with ``ServiceRegistry.configure(some_registry)``
    and then use it elsewhere in code via ``ServiceRegistry.get()``.
    """

    __instance = None  # access it via ServiceRegistry.get()

    @classmethod
    def get(cls) -> "ServiceRegistry":
        """
        :return: configured global service registry instance
        :raise LookupError: if registry was not configured yet
        """
        instance = cls.__instance
        if not instance:
            message = "Service discovery is not configured yet." \
                      " Call ServiceRegistry.configure(some_instance) at the beginning of the program."
            raise LookupError(message)
        return instance

    @classmethod
    def configure(cls, configured: "ServiceRegistry") -> None:
        """
        :param ServiceRegistry configured: global instance to be used wherever in the app
        """
        if cls.__instance:
            raise ValueError("Service discovery instance is already configured."
                             " It's forbidden to switch instance at runtime"
                             " to prevent unpredictable behavior.")
        cls.__instance = configured

    @abstractmethod
    def linkedin(self) -> LinkedInClient:
        """Proper LinkedIn client."""

    @abstractmethod
    def news_storage(self) -> NewsStorage:
        """Proper LinkedIn client."""


class ConfigDrivenServiceRegistry(ServiceRegistry):
    """Service registry that uses app's config to get proper clients."""

    def __init__(self, options: ConfigParser) -> None:
        self.options = options

    def linkedin(self) -> LinkedInClient:
        return self._cached_linkedin

    @cached_property
    def _cached_linkedin(self):
        if self.options.getboolean("linkedin", "disabled"):
            return FakeLinkedInClient()
        return RestLinkedInClient(
            base_url=options.get("linkedin", "url"),
            client_id=options.get("linkedin", "client-id"),
            client_secret=options.get("linkedin", "client-secret"),
            redirect_uri=options.get("linkedin", "redirect-uri"),
            auth_path=options.get("linkedin", "auth-path"),
            token_path=options.get("linkedin", "token-endpoint"),
            api_url=options.get("linkedin", "api-url")
        )

    def news_storage(self):
        return self._cached_news_storage

    @cached_property
    def _cached_news_storage(self) -> NewsStorage:
        return DjangoORMBasedStorage()
