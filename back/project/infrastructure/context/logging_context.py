import os, logging

from project.adapters.logging_middleware_adapters import LoggingMiddlewareAdapters

class LoggingContext(LoggingMiddlewareAdapters):
    def get_module_logging(self):
        path = os.path.abspath("project/static/logging.txt")
        """path = os.path.abspath("project/static/logging.txt")
        file_ = open(path)"""
        """ source = logging.basicConfig(
            filename=path, encoding="utf-8", level=logging.DEBUG
        ) """
        source = logging
        source.basicConfig(
            filename=path, encoding="utf-8", level=logging.DEBUG
        )
        return source