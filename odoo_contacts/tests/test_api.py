import asyncio

import pytest
from httpx import AsyncClient

from odoo_contacts.main import create_app


# @pytest.fixture(scope="session")
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()
#
#
# @pytest.fixture(scope="session")
# def app():
#     app = create_app(config='TESTING')
#     return app
#
#
# @pytest.fixture(scope="function")
# async def ac(app):
#     """Async Client for testing endpoints"""
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#
#         yield ac

from fastapi.testclient import TestClient

from odoo_contacts.main import create_app

ac = TestClient(create_app(config="TESTING"))


@pytest.mark.parametrize("email,password,status_code", [
    ("cat@dog.com", "catdog", 201),
    ("cat@dog.com", "cat0dog", 409),
    ("dog@cat.com", "dogcat", 201),
    ("abcde", "dogcat", 422),
])
def test_register_user(email, password, status_code):
    response = ac.post("/auth/signup", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("test@test.com", "test", 200),
    ("user@example.com", "user", 200),
    ("wrong@person.com", "wrong", 401),
])
def test_login_user(email, password, status_code):
    response = ac.post("/auth/login", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code


