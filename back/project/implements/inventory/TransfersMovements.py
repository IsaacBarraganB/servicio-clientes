from project.adapters.inventory.MovementsAdapter import MovementsAdapter
from project.implements.inventory.Movements import Movements
from decimal import Decimal
from project.implements.logging_implementations import LoggingImplementations
from project.infrastructure.context.logging_context import LoggingContext

class TransfersMovements(MovementsAdapter):
    #next: MovementsAdapter
    def __init__(self):
        self.next = None
    
    
    def nextMovement(self, next: MovementsAdapter) -> None:
        self.next = next

    
    def executeMovement(self, movement: Movements) -> None:
        try:
            if movement.typeMovement == 'TRASPASO':
                #modelo movement
                modelMovement = movement.movement
                #modelo detalle del movimiento
                modelMovementDetails = movement.movement_details
                #modelo stock
                modelStock = movement.stock

                movementInfo = movement.repository.query(modelMovement).filter_by(
                    id=movement.movement_id
                ).first()
                
                if not movementInfo:
                    return {"data": "Movimiento no encontrado.", "result": False}

                if movementInfo.status_movement_id == 1:
                    articlesDetails = movement.repository.query(modelMovementDetails).filter(
                        modelMovementDetails.movement_id==movement.movement_id
                    ).all()
                    if not articlesDetails:
                        return {"data": "No hay detalles del movimiento.", "result": False}
                    errors = []
                    for items in articlesDetails:
                        success, message = self.update_or_insert_stock(
                            store_id=movementInfo.store_id,
                            repository=movement.repository,
                            account_id=movementInfo.account_id,
                            article_id=items.article_id,
                            modelStock=modelStock,
                            destination_store_id=movementInfo.destination_store_id,
                            quantity=items.quantity
                        )
                        if not success:
                            errors.append(message)
                    if errors:
                        return {"data": f"Errores en los artículos: {errors}", "result": False}
                    movementInfo.status_movement_id = 2
                    movement.repository.commit()
                    return {"data": f'El movimiento ha sido ejecutado.', "result": True}
            else:
                return self.next.executeMovement(movement)
        except Exception as e:
            account_id = movementInfo.account_id if movementInfo else "Desconocido"
            log = LoggingImplementations(LoggingContext())
            log.error(f'Error al ejecutar el movimiento {movement.movement_id} - ({movement.typeMovement}) - Cuenta:{account_id} - {e}')
            return {"data": f"Ocurrió un error al procesar el movimiento. Por favor, contacte al soporte.: {str(e)}", "result": False}
    

    def update_or_insert_stock(self, repository, modelStock, destination_store_id, store_id, article_id, quantity, account_id):
        try:
            if not isinstance(quantity, Decimal):
                quantity = Decimal(str(quantity))
            stock_local = repository.query(modelStock).filter_by(store_id=store_id, article_id=article_id).first()
            stock_destination = repository.query(modelStock).filter_by(store_id=destination_store_id, article_id=article_id).first()
            # Validar sì hay stock por parte de el almacen local
            if not stock_local or stock_local.stock < quantity:
                available_stock = stock_local.stock if stock_local else 0
                return False, f"Stock insuficiente para el artículo {article_id}. Disponible: {available_stock}, Requerido: {quantity}."
            
            stock_local.stock -= quantity
            if stock_destination:
                stock_destination.stock += quantity
            else:
                new_stock = modelStock(
                    store_id=destination_store_id,
                    article_id=article_id,
                    stock=quantity,
                    account_id=account_id,
                )
                repository.add(new_stock)
                

            return True, f"Stock actualizado correctamente. Origen: {store_id}, Destino: {destination_store_id}, Artículo: {article_id}, Cantidad: {quantity}."
        except Exception as e:
            log = LoggingImplementations(LoggingContext())
            log.error(f"Error al actualizar stock de la cuenta {account_id} para artículo {article_id} (Origen: {store_id}, Destino: {destination_store_id}): {e}")
            return False, f"Error al actualizar stock: {str(e)}"

