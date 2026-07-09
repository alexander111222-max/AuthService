from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.config import settings

Base = declarative_base()


engine = create_async_engine(settings.DB_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


engine_null_pool = create_async_engine(settings.DB_URL, poolclass=NullPool)
async_session_maker_null_pool = async_sessionmaker(engine_null_pool, expire_on_commit=False)






