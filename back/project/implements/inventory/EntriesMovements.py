from project.adapters.inventory.MovementsAdapter import MovementsAdapter
from project.implements.inventory.Movements import Movements
from decimal import Decimal

#MOVIMIENTOS ENTRADAS
class EntriesMovements(MovementsAdapter):
    def __init__(self):
        self.next = None
    
    
    def nextMovement(self, next: MovementsAdapter) -> None:
        self.next = next

    
    def executeMovement(self, movement: Movements) -> None:
        if movement.typeMovement == 'ENTRADA':
            #modelo movement
            modelMovement = movement.movement
            #modelo detalle del movimiento
            modelMovementDetails = movement.movement_details
            #modelo stock
            modelStock = movement.stock

            movementInfo = movement.repository.query(modelMovement).filter_by(id=movement.movement_id).first()
            store_id = movementInfo.store_id
            account_id = movementInfo.account_id

            if movementInfo.status_movement_id == 1:
                detailsArticles = movement.repository.query(modelMovementDetails).filter(modelMovementDetails.movement_id==movement.movement_id)
                for items in detailsArticles.all():
                    self.update_or_insert_stock(
                        store_id=store_id,
                        repository=movement.repository,
                        account_id=account_id,
                        article_id=items.article_id,
                        modelStock=modelStock,
                        quantity=items.quantity
                    )
                movementInfo.status_movement_id = 2
                movement.repository.commit()
                return {"data": f'El movimiento ha sido ejecutado.', "result": True}
            else:
                return {"data": f'El movimiento no puede ejecutarse.', "result": False}
        else:
            return self.next.executeMovement(movement)

    
    def update_or_insert_stock(self, repository, modelStock, store_id, article_id, quantity, account_id):
        if not isinstance(quantity, Decimal):
            quantity = Decimal(str(quantity))
        stock_entry = repository.query(modelStock).filter_by(store_id=store_id, article_id=article_id).first()
        if stock_entry:
            # Si el stock existe, actualiza el valor
            stock_entry.stock += quantity
        else:
            # Si no existe, crea una nueva entrada
            new_stock = modelStock(
                store_id=store_id,
                article_id=article_id,
                stock=quantity,
                account_id=account_id
            )
            repository.add(new_stock)



