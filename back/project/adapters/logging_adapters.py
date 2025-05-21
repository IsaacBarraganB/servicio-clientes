import abc

class LoggingAdapters(abc.ABC):
    @abc.abstractmethod
    def debug(self, message):
        """
        An abstract method A
        """
        return NotImplementedError

    @abc.abstractmethod
    def info(self, message):
        """
        An abstract method A
        """
        return NotImplementedError

    @abc.abstractmethod
    def warning(self, message):
        """
        An abstract method A
        """
        return NotImplementedError

    @abc.abstractmethod
    def error(self, message):
        """
        An abstract method A
        """
        return NotImplementedError

    @abc.abstractmethod
    def critical(self, message):
        """
        An abstract method A
        """
        return NotImplementedError