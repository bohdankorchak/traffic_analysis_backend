import asyncio

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from backend.app.models import Base


ADMIN_DATABASE_URL = "postgresql+asyncpg://traffic_user:traffic_password@localhost:5432/postgres"
TEST_USER = "test_user"
TEST_PASSWORD = "test_password"
TEST_DATABASE = "test_db"


@pytest.fixture(scope="session", autouse=True)
async def test_db():
    """Setup and teardown for the test database."""
    admin_engine = create_async_engine(ADMIN_DATABASE_URL, isolation_level="AUTOCOMMIT")
    async with admin_engine.connect() as conn:
        # Drop active connections and recreate the test database
        await conn.execute(
            text(f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{TEST_DATABASE}'
                  AND pid <> pg_backend_pid();
            """)
        )
        await conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DATABASE}"))
        await conn.execute(text(f"DROP USER IF EXISTS {TEST_USER}"))
        await conn.execute(
            text(f"CREATE USER {TEST_USER} WITH PASSWORD '{TEST_PASSWORD}'")
        )
        await conn.execute(
            text(f"CREATE DATABASE {TEST_DATABASE} OWNER {TEST_USER}")
        )
        await conn.execute(
            text(f"GRANT ALL PRIVILEGES ON DATABASE {TEST_DATABASE} TO {TEST_USER}")
        )

    test_engine = create_async_engine(
        f"postgresql+asyncpg://{TEST_USER}:{TEST_PASSWORD}@localhost:5432/{TEST_DATABASE}",
        echo=True
    )

    # Bind models to the test database
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield test_engine

    # Teardown: Drop the test database
    async with admin_engine.connect() as conn:
        await conn.execute(
            text(f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{TEST_DATABASE}'
                  AND pid <> pg_backend_pid();
            """)
        )
        await conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DATABASE}"))
        await conn.execute(text(f"DROP USER IF EXISTS {TEST_USER}"))
