import os
import logging
from typing import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

logger = logging.getLogger("database")

DB_DRIVER = os.getenv("DB_DRIVER", "sqlite")
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
        
        # SQLite schema auto-migration for newly added columns in PRD v8.0
        if "sqlite" in DATABASE_URL:
            # Columns to ensure in 'test_runs' table
            new_run_cols = [
                ("estimated_manual_hours", "FLOAT DEFAULT 0.0"),
                ("automated_hours", "FLOAT DEFAULT 0.0"),
                ("human_review_hours", "FLOAT DEFAULT 0.0"),
                ("effort_reduction_percentage", "FLOAT DEFAULT 0.0"),
                ("effort_metrics", "JSON DEFAULT '{}'"),
                ("coverage_summary", "JSON DEFAULT '{}'"),
                ("test_budget", "JSON DEFAULT '{}'"),
                ("onboarding_mode", "VARCHAR DEFAULT 'URL'"),
            ]
            for col_name, col_type in new_run_cols:
                try:
                    await conn.execute(text(f"ALTER TABLE test_runs ADD COLUMN {col_name} {col_type}"))
                except Exception:
                    pass

            # Columns to ensure in 'findings' table
            new_finding_cols = [
                ("confidence_score", "FLOAT DEFAULT 95.0"),
                ("remediation_diff", "TEXT"),
                ("retest_verdict", "VARCHAR"),
                ("evidence_hash", "VARCHAR"),
                ("is_human_review_required", "BOOLEAN DEFAULT 0"),
                ("human_review_notes", "TEXT"),
            ]
            for col_name, col_type in new_finding_cols:
                try:
                    await conn.execute(text(f"ALTER TABLE findings ADD COLUMN {col_name} {col_type}"))
                except Exception:
                    pass

            # Columns to ensure in 'policies' table
            new_policy_cols = [
                ("policy_level", "VARCHAR DEFAULT 'STANDARD'"),
                ("allowed_domains", "JSON DEFAULT '[]'"),
                ("allowed_ips", "JSON DEFAULT '[]'"),
                ("allowed_methods", "JSON DEFAULT '[]'"),
                ("allowed_test_classes", "JSON DEFAULT '[]'"),
            ]
            for col_name, col_type in new_policy_cols:
                try:
                    await conn.execute(text(f"ALTER TABLE policies ADD COLUMN {col_name} {col_type}"))
                except Exception:
                    pass

            # Columns to ensure in 'projects' table
            new_project_cols = [
                ("target_owner", "VARCHAR"),
                ("target_url", "VARCHAR"),
                ("environment", "VARCHAR DEFAULT 'DEV'"),
                ("policy_level", "VARCHAR DEFAULT 'STANDARD'"),
                ("authorization_status", "VARCHAR DEFAULT 'AUTHORIZED'"),
                ("authorized_domains", "JSON DEFAULT '[]'"),
                ("authorized_ip_ranges", "JSON DEFAULT '[]'"),
                ("authorized_endpoints", "JSON DEFAULT '[]'"),
                ("testing_window", "VARCHAR DEFAULT 'ANYTIME'"),
            ]
            for col_name, col_type in new_project_cols:
                try:
                    await conn.execute(text(f"ALTER TABLE projects ADD COLUMN {col_name} {col_type}"))
                except Exception:
                    pass

            # Columns to ensure in 'targets' table
            new_target_cols = [
                ("target_owner", "VARCHAR"),
                ("authorization_status", "VARCHAR DEFAULT 'AUTHORIZED'"),
                ("authorized_domains", "JSON DEFAULT '[]'"),
                ("authorized_ip_ranges", "JSON DEFAULT '[]'"),
                ("authorized_endpoints", "JSON DEFAULT '[]'"),
                ("testing_window", "VARCHAR DEFAULT 'ANYTIME'"),
                ("max_test_intensity", "VARCHAR DEFAULT 'STANDARD'"),
            ]
            for col_name, col_type in new_target_cols:
                try:
                    await conn.execute(text(f"ALTER TABLE targets ADD COLUMN {col_name} {col_type}"))
                except Exception:
                    pass
