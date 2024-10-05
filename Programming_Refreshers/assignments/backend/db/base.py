import sqlalchemy
from sqlalchemy.orm import DeclarativeBase

from backend.settings import settings

meta = sqlalchemy.MetaData(schema=settings.db_schema)


class Base(DeclarativeBase):
    """Base for all DB models."""

    metadata = meta
