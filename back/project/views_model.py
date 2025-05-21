from sqlalchemy import Table

from project.infrastructure.repository import engine
from project.models import Base
from sqlalchemy import Column, Integer


def _init_table(name, columns: list = []):
    columns = [Column("id", Integer, primary_key=True)] + columns
    return Table(
        name,
        Base.metadata,
        *columns,
        autoload_with=engine,
    )


def _primary(__table__):
    return {"primary_key": [__table__.c.id]}
