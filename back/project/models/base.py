
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import declared_attr, declarative_base
Base = declarative_base()
class Model(Base):
    """This abstract class base"""

    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, nullable=False)
    created_on = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    modified_on = Column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )