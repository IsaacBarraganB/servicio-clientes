from abc import ABC, abstractmethod
from project.implements.inventory.Movements import Movements

class MovementsAdapter(ABC):
    @abstractmethod
    def nextMovement(self, next: 'MovementsAdapter') -> None:
        pass

    @abstractmethod
    def executeMovement(movement: 'Movements') -> None:
        pass