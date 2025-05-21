from abc import ABC, abstractmethod

class ReceiptAdapter(ABC):
    @abstractmethod
    def change_status(self, id, schema, config, compose):
        pass