from project.utils.general_utils import GeneralUtils
from project.utils.constants import Constants
from project.utils.sqlalchemy_utils import SQLAlchemyUtils
from project.settings import Settings
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
import json
from project.implements.logging_implementations import LoggingImplementations
from project.infrastructure.context.logging_context import LoggingContext
from passlib.hash import pbkdf2_sha256
class Compose:
    def __init__(
        self,
        model:any=None,
        notify:str=None,
        repository=None,
        settings:Settings=None,
        generalUtils:GeneralUtils=None,
        constants:Constants=None,
        config=None
    ) -> None:
        self.model = model
        self.notify = notify
        self.repository = repository
        self.settings = settings
        self.generalUtils = generalUtils
        self.constants = constants
        self.config= config

    def pagination(self, filter, or_filters, pagination, columns):
        try:
            statement = self.repository.query(self.model)

            if columns:
                cols = SQLAlchemyUtils.get_model_columns(model=self.model, columns=columns)
                statement = statement.with_entities(*cols)
            statement = SQLAlchemyUtils.build_filter(model=self.model, statement=statement, filter=filter, or_filters=or_filters, config=self.config)
            total_items = statement.count()
            if pagination:
                pagination = json.loads(pagination)
                statement = SQLAlchemyUtils.build_paginate(model=self.model, statement=statement, pagination=pagination)
            
            items = statement.all()
            if columns:
                items = [dict(zip(columns, item)) for item in items]
            return {
                "result": True,
                "rowsCount": total_items,
                "data": items
            }
        except (SQLAlchemyError, AttributeError, ValueError) as e:
            log = LoggingImplementations(LoggingContext())
            log.error(f'Pagination error: {e}')
            return {"error": str(e)}
        

    def getAll(self, filter):
        print(filter)
        return "GetAll"

    def create(self, schema, refresh: bool = False):
        arguments = self.generalUtils.schema_to_dict(schema=schema)
        # Add account_id
        if arguments:
            if hasattr(schema, "account_id"):
                pass
            elif hasattr(self.model, "account_id"):
                arguments['account_id'] = self.config['account_id']

        try:
            if self.model and self.repository:
                model = self.model(**arguments)
                self.repository.add(model)
                self.repository.commit()
                if refresh:
                    self.repository.refresh(model)
        except SQLAlchemyError as e:
            self.repository.rollback()
            log = LoggingImplementations(LoggingContext())
            error_code = getattr(e.orig, 'pgcode', None)
            log.error(f'Create error: {e}')
            return {"error": str(e), "code": error_code}

        return {"data": f'{self.notify} ha sido creado.', "result": True}

    def update(self, id, schema):
        try:
            if self.model and self.repository:
                to_update = self.repository.query(self.model).filter_by(id=id).first()
                for field_name, value in schema.dict().items():
                    if field_name == 'password' and value:
                        value = pbkdf2_sha256.hash(value)
                        setattr(to_update, field_name, value)
                    else:
                        if value is not None:  # Asegurarse de que no se asignen valores nulos
                            setattr(to_update, field_name, value)
                if to_update:
                    self.repository.commit()
        except SQLAlchemyError as e:
            self.repository.rollback()
            log = LoggingImplementations(LoggingContext())
            log.error(f'Update error: {e}')
            return {"error": str(e)}
        
        return {"data": f'{self.notify} ha sido actualizado.', "result": True}

    def delete(self, id):
        try:
            if self.model and self.repository:
                to_delete = self.repository.get(self.model, id)
                if to_delete:
                    self.repository.delete(to_delete)
                    self.repository.commit()
        except SQLAlchemyError as e:
            self.repository.rollback()
            log = LoggingImplementations(LoggingContext())
            log.error(f'Delete error: {e}')
            return {"error": str(e)}
        
        return {"data": f'{self.notify} ha sido eliminado.'}