import logging

from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.schema import CreateSchema
from sqlalchemy_utils import create_database, database_exists

from backend.db.curd.user import create_admin_entry
from backend.settings import settings

from .base import meta

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def _create_database(enginee: Engine) -> None:
    logger.info("Creating Database .....")

    if not database_exists(enginee.url):
        logger.info("Database not exists Creating a new one.....")
        create_database(enginee.url)
    else:
        logger.info("Database exists .....")
    return None


def _create_schema(enginee: Engine) -> None:  # pragma: no cover
    """Populates tables in the database."""
    logger.info("Creating Db Schama .....")
    logger.info(f"DB Schama {settings.db_schema}")
    if settings.db_schema is None:
        return None
    with enginee.begin() as connection:
        schema_exists = enginee.dialect.has_schema(connection=connection, schema_name=settings.db_schema)
        if not schema_exists:
            return_code = connection.execute(CreateSchema(settings.db_schema))
            logger.info(f"return_code {return_code}")


def _create_tables(enginee: Engine) -> None:
    """Populates tables in the database."""
    logger.info("Creating Db Tables .....")

    with enginee.begin() as connection:
        # return_code = connection.execute(meta.create_all, checkfirst=True)
        return_code = meta.create_all(connection, checkfirst=True)
        logger.info(f"return_code {return_code}")


def _insrt_entry(enginee: Engine):
    logger.info("inserting Entries to Tables .....")
    with Session(enginee) as session:
        create_admin_entry(session)
        session.commit()


def establish_db():
    _db_url = URL.create(drivername="sqlite", database=settings.db_name)
    logger.info(f"DB URL {_db_url}")
    engine = create_engine(_db_url, echo=True)
    _create_database(engine)
    _create_schema(engine)
    _create_tables(engine)
    _insrt_entry(engine)
    engine.dispose()


if __name__ == "__main__":
    establish_db()
