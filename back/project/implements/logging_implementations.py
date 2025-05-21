from project.adapters.logging_adapters import LoggingAdapters
from project.adapters.logging_middleware_adapters import LoggingMiddlewareAdapters
import datetime

class LoggingImplementations(LoggingAdapters):
    middleware_adapter = LoggingMiddlewareAdapters
    date_current = datetime.datetime.now()
    def __init__(self, middleware_adapter):
        self.client = middleware_adapter.get_module_logging()

    def warning(self, message):
        self.client.warning(f"{message} - Time {self.date_current}")

    def critical(self, message):
        self.client.critical(f"{message} - Time {self.date_current}")

    def error(self, message):
        self.client.error(f"{message} - Time {self.date_current}")

    def info(self, message):
        self.client.info(f"{message} - Time {self.date_current}")

    def debug(self, message):
        self.client.message(f"{message} - Time {self.date_current}")