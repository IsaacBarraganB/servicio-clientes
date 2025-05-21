class Movements:
    def __init__(self, movement, movementDetails, stock, repository, movement_id: int, typeMovement: str):
        self._movement_id = movement_id
        self._typeMovement = typeMovement
        self._movement = movement
        self._movementDetails = movementDetails
        self._stock = stock
        self._repository = repository
    
    @property
    def movement_id(self):
        return self._movement_id
    
    @movement_id.setter
    def movement_id(self, movement_id: int):
        self._movement_id = movement_id

    
    @property
    def typeMovement(self):
        return self._typeMovement
    
    @typeMovement.setter
    def typeMovement(self, typeMovement: str):
        self._typeMovement = typeMovement
    
    @property
    def movement(self):
        return self._movement
    
    @property
    def movement_details(self):
        return self._movementDetails
    
    @property
    def stock(self):
        return self._stock
    
    @property
    def repository(self):
        return self._repository