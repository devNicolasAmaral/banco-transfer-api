from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from app.core.config import settings


database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=settings.postgres_user,
    password=settings.postgres_password,
    database=settings.postgres_db,
    host=settings.postgres_host,
    port=settings.postgres_port,
)

engine = create_engine(database_url, echo=True)
