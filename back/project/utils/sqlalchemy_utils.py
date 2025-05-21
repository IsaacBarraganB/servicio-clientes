from sqlalchemy import asc, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
import json

SQLALCHEMY_OPERATOR_MAP = {
        "=": lambda column, val: column == val,
        "==": lambda column, val: column == val,
        "equals": lambda column, val: column == val,
        "eq": lambda column, val: column == val,
        "!=": lambda column, val: column != val,
        "<>": lambda column, val: column != val,
        "ne": lambda column, val: column != val,
        "notequals": lambda column, val: column != val,
        "<": lambda column, val: column < val,
        "lt": lambda column, val: column < val,
        ">": lambda column, val: column > val,
        "gt": lambda column, val: column > val,
        "<=": lambda column, val: column <= val,
        "le": lambda column, val: column <= val,
        ">=": lambda column, val: column >= val,
        "ge": lambda column, val: column >= val,
        "ilike": lambda column, val: column.ilike(f'%{val}%'),
    }
class SQLAlchemyUtils:
    def build_filter(model, statement, filter, or_filters, config):
        if filter:
            filter = json.loads(filter)
            if hasattr(model, "account_id"):
                if any("account_id" in field for field in filter):
                    pass
                else:
                    filter.append(['account_id', '=', config['account_id']])

            for value in filter:
                key, operator, val = value

                column = getattr(model, key)

                if operator in SQLALCHEMY_OPERATOR_MAP:
                    statement = statement.filter(SQLALCHEMY_OPERATOR_MAP[operator](column, val))
                else:
                    raise ValueError(f"Operador no soportado: {operator}")
        else:
            if hasattr(model, "account_id"):
                key, operator, val = ['account_id', '=', config['account_id']]
                column = getattr(model, key)

                if operator in SQLALCHEMY_OPERATOR_MAP:
                    statement = statement.filter(SQLALCHEMY_OPERATOR_MAP[operator](column, val))
                else:
                    raise ValueError(f"Operador no soportado: {operator}")
                

        
        if or_filters:
            or_filters = json.loads(or_filters)
            or_conditions = []
            for value in or_filters:
                key, val = value
                column = getattr(model, key)
                or_conditions.append(SQLALCHEMY_OPERATOR_MAP["ilike"](column, val))
            statement = statement.filter(or_(*or_conditions))
        return statement
    
    def build_paginate(model, statement, pagination):
        if pagination['sortBy']:
            sort_order = desc if not pagination['descending'] == True else asc
            statement = statement.order_by(sort_order(getattr(model, pagination['sortBy'])))

        rows_per_page = pagination['rowsPerPage']
        current_page = pagination['page']
        statement = statement.limit(rows_per_page).offset((current_page -1) * rows_per_page )

        return statement
    

    def get_model_columns(model, columns: list | tuple) -> list:
        result = [
            getattr(model, column) if isinstance(column, str) else column
            for column in columns
        ]
        return result
        
            