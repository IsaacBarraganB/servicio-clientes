from project.adapters.inventory.MovementsAdapter import MovementsAdapter
from project.implements.inventory.Movements import Movements
from decimal import Decimal

#MOVIMIENTOS SALIDAS
class ExitsMovements(MovementsAdapter):
    def __init__(self):
        self.next = None
    
    
    def nextMovement(self, next: MovementsAdapter) -> None:
        self.next = next

    
    def executeMovement(self, movement: Movements) -> None:
        if movement.typeMovement == 'SALIDA':
            #modelo movement
            modelMovement = movement.movement
            #modelo detalle del movimiento
            modelMovementDetails = movement.movement_details
            #modelo stock
            modelStock = movement.stock

            movementInfo = movement.repository.query(modelMovement).filter_by(id=movement.movement_id).first()
            store_id = movementInfo.store_id

            if movementInfo.status_movement_id == 1:
                detailsArticles = movement.repository.query(modelMovementDetails).filter(modelMovementDetails.movement_id==movement.movement_id)
                errosInfo = []
                execute = True
                for items in detailsArticles.all():
                    status, message= self.update_stock(
                        store_id=store_id,
                        repository=movement.repository,
                        article_id=items.article_id,
                        modelStock=modelStock,
                        quantity=items.quantity
                    )
                    if not status:
                        execute = False
                        errosInfo.append(message)
                if execute:
                    movementInfo.status_movement_id = 2
                    movement.repository.commit()
                    return {"data": f'El movimiento ha sido ejecutado.', "result": True}
                else:
                    return {"data": f'El movimiento no ha sido ejecutado.', "result": False, "errors": errosInfo}

            else:
                return {"data": f'El movimiento ya se encuentra ejecutado.', "result": False}
        else:
            return self.next.executeMovement(movement)
    

    def update_stock(self, repository, modelStock, store_id, article_id, quantity):
        try:
            if not isinstance(quantity, Decimal):
                quantity = Decimal(str(quantity))
            stock_entry = repository.query(modelStock).filter_by(store_id=store_id, article_id=article_id).first()
            if not stock_entry:
                return False, f"Entrada de stock no encontrada store_id={store_id} y article_id={article_id}."
            
            if stock_entry.stock < quantity:
                return False, f"Stock insuficiente article_id={article_id}. Disponible: {stock_entry.stock}, Requerido: {quantity}."
            
            stock_entry.stock -= quantity
            return True, f"Stock actualizado correctamente article_id={article_id}. Existencia: {stock_entry.stock}."

        except Exception as e:
            return False, f"An error occurred: {str(e)}"

