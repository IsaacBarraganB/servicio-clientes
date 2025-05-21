from project.adapters.receipt.ReceiptAdapter import ReceiptAdapter
from sqlalchemy.exc import SQLAlchemyError
from project.views.inv.inv_movements import __get_service__ as service_movement
from project.views.inv.inv_movements_details import __get_service__ as service_movement_details
from project.views.pur.pur_orders import __get_service__ as service_orders
from project.views.pur.pur_orders_details import __get_service__ as service_orders_details
from project.views.pur.pur_received_details import __get_service__ as service_received_details
from project.implements.logging_implementations import LoggingImplementations
from project.infrastructure.context.logging_context import LoggingContext
from datetime import datetime
from sqlalchemy import text
import pytz
class ReceiptExecute(ReceiptAdapter):
    def change_status(self, id, schema, config=None, compose=None):
        # Actualizar receipt a executado, Crear movement, Crear movements_details, Ejecutar movement
        try:
            if compose.model and compose.repository:
                # Busca la recepcion
                receipt = compose.repository.query(compose.model).filter_by(id=id).first()
                for field_name, value in schema.dict().items():
                    setattr(receipt, field_name, value)
                if not receipt:
                    return {"data": f'No se encontrò {compose.notify}', "result": False}
                # Busca la orden de compra
                order = service_orders()
                data_order = order.compose.repository.query(order.compose.model).filter_by(id=receipt.order_id).first()
                if not data_order:
                    return {"data": f'No se encontrò la order de compra', "result": False}
                # Crear movimiento
                timezone = pytz.timezone("America/Mexico_City")
                now = datetime.now(timezone)
                formatted_date = now.strftime("%Y-%m-%d %H:%M:%S.%f %z")

                data_movement = {
                    'type_movement_id': 1,
                    'store_id': data_order.store_id,
                    'status_movement_id': 1,
                    'destination_store_id': None,
                    'date':formatted_date
                    }
                movements = service_movement(config=config)
                result_movement = movements.create_with_folio(schema=data_movement)

                # Busca los articulos de la recepcion
                received_details = service_received_details()
                data_received_details = received_details.compose.repository.query(received_details.compose.model).filter_by(receipt_id=receipt.id)
                if not data_received_details:
                    return {"data": f'No se encontraron detalles de la recepciòn', "result": False}
                
                # Busca los detalles de la orden
                order_details = service_orders_details()
            
                movements_details = service_movement_details()

                values_clause = []
                params = {}
                
                for i, detail in enumerate(data_received_details):
                    data_order_details = order_details.compose.repository.query(order_details.compose.model).filter_by(id=detail.detail_id).first()
                    # Asigna nombres de parámetros únicos para cada detalle
                    account_id = f"account_id_{i}"
                    article_id = f"article_id_{i}"
                    cost = f"cost_{i}"
                    movement_id = f"movement_id_{i}"
                    quantity = f"quantity_{i}"
                    
                    # Construye la parte VALUES de la consulta
                    values_clause.append(f"(:{article_id}, :{quantity},  :{cost}, :{account_id},:{movement_id})")
                    
                    # Agrega los parámetros al diccionario
                    params[account_id] = data_order_details.account_id
                    params[article_id] = data_order_details.article_id
                    params[cost] = data_order_details.price
                    params[movement_id] = result_movement['id']
                    params[quantity] = detail.quantity

                query = text(f"""
                        INSERT INTO inv_movements_details (article_id, quantity, cost, account_id, movement_id)
                        VALUES {', '.join(values_clause)}
                    """)
                movements.compose.repository.commit()
                add_movement_details = movements_details.compose.repository.execute(query, params)
                movements_details.compose.repository.commit()
                if not add_movement_details:
                    return {"data": f'No se pudieron agregar los articulos a la orden', "result": False}
                movements_execute = service_movement(config=config)
                movements_execute.execute_movement(movement_id=result_movement['id'], type_movement="ENTRADA")
                receipt.movement_id = result_movement['id']
                compose.repository.commit()
        except SQLAlchemyError as e:
            compose.repository.rollback()
            log = LoggingImplementations(LoggingContext())
            error_code = getattr(e.orig, 'pgcode', None)
            log.error(f'Update error: {e}')
            return {"error": str(e), "code": error_code}
        return {"data": f'{compose.notify} ha sido modificado.', "result": True}