import abc
class LoggingMiddlewareAdapters(abc.ABC):
    @abc.abstractmethod
    def get_module_logging(self):
        raise NotImplementedError