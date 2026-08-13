import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declarative_base

# Database URL configuration: Support PostgreSQL production and SQLite fallback/development mode
DB_DRIVER = os.getenv("DB_DRIVER", "sqlite") # "postgresql" or "sqlite"
POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/testing_engineer")
SQLITE_URL = os.getenv("SQLITE_URL", "sqlite+aiosqlite:///./testing_engineer.db")

if DB_DRIVER == "postgresql":
    DATABASE_URL = POSTGRES_URL
else:
    DATABASE_URL = SQLITE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
