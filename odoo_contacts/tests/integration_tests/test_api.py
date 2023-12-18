import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email,password,status_code", [
    ("test@one.com", "testone", 201),
    ("test@one.com", "test1one", 409),
    ("one@test.com", "onetest", 201),
    ("abcde", "test12", 422),
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/api/v1/auth/signup", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("test@test.com", "test", 200),
    ("igor@example.com", "igor", 401),
    ("wrong@person.com", "igor", 401),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/api/v1/auth/login", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code
