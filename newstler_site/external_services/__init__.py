"""Some initial actions for external services"""
import logging

from newstler_site.config import define_options
from newstler_site.external_services.service_registry import ServiceRegistry, ConfigDrivenServiceRegistry


LOG = logging.getLogger('consolelogger')
options = define_options()
service_registry = ConfigDrivenServiceRegistry(options)
ServiceRegistry.configure(service_registry)
