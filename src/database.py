from typing import cast, AsyncGenerator

from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from asyncpg import connect

from config import APP_ASYNC_DRIVER, PG_DB_NAME, PG_HOST, PG_PASS, PG_PORT, PG_USER

# PostgreSQL
engine = create_async_engine(
    url=f'{APP_ASYNC_DRIVER}://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}',
    echo=True
)

async_session = sessionmaker(
    cast(Engine, engine),
    class_=cast(Session, AsyncSession),
    autoflush=False,
    expire_on_commit=False,
    autocommit=False,
)


#async def session_generator() -> AsyncSession:
 #   async with async_session() as session:
#        yield session


async def ping_postgres_database():
    """Ping database"""
    try:
        connection = await connect(
            database=PG_DB_NAME,
            user=PG_USER,
            password=PG_PASS,
            host=PG_HOST,
            port=PG_PORT,
        )
        await connection.close()
    except ConnectionRefusedError as e:
        raise ConnectionRefusedError(
            'Connect to database error!'
        ) from e
