import psycopg2
import time
from loguru import logger

from core.config import settings


def wait_for_postgres():
    while True:
        try:
            url = f"postgres://{settings.db.host}:{settings.db.port}/{settings.db.database}"
            logger.info(f"Connecting with url: {url}")
            conn = psycopg2.connect(
                dbname=settings.db.database,
                user=settings.db.username,
                password=settings.db.password.get_secret_value(),
                host=settings.db.host,
                port=settings.db.port,
            )
            conn.close()
            logger.info("PostgreSQL is ready.")
            break
        except psycopg2.OperationalError:
            logger.info("Waiting for PostgreSQL to be ready...")
            time.sleep(1)


if __name__ == "__main__":
    wait_for_postgres()
