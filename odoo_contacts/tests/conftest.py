import asyncio
import json
import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from odoo_contacts.core.models import Contact
from odoo_contacts.config import settings
from odoo_contacts.sql.database import Base, async_session_maker, engine
from odoo_contacts.main import app as fastapi_app
from odoo_contacts.users.models import User


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    """Preparing test DB """
    assert settings.MODE == 'TEST'

    async with engine.begin() as conn:
        # Drop all test tables
        await conn.run_sync(Base.metadata.drop_all)
        # Create all test tables
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    users = open_mock_json("users")
    contacts = open_mock_json("contacts")

    async with async_session_maker() as session:
        for Model, values in [
            (User, users),
            (Contact, contacts),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    """Async client for testing endpoints"""
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    """Async authenticated client for testing endpoints"""
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/api/v1/auth/login", json={
            "email": "test@test.com",
            "password": "test",
        })
        assert ac.cookies["oddo_contacts_access_token"]
        yield ac
