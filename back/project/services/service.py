
from project.composers.compose import Compose
class Service:
    compose: Compose
    def __init__(self, compose):
        self.compose = compose
    
    def pagination(self, filter, or_filters, pagination, columns=None):
        result = self.compose.pagination(filter=filter, or_filters=or_filters, pagination=pagination, columns=columns)
        return result
    
    # queda pendiente en el compose
    def getAll(self, filter):
        result = self.compose.getAll(filter=filter)
        return result
    
    def create(self, schema: any, refresh: bool = False):
        result = self.compose.create(schema=schema, refresh=refresh)
        return result
    
    def update(self, id: int, schema: any):
        result = self.compose.update(id, schema=schema)
        return result
    
    def delete(self, id):
        result = self.compose.delete(id=id)
        return result