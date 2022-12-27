import json

from fastapi.encoders import jsonable_encoder

from app.api import user
from app.main import app
from app.schemas.user import UserOut
from app.services.auth import get_current_user

TEST_USER = UserOut(
    **{
        "username": "test_user",
        "email": "supertest@gmail.com",
        "id": "476e386c-1234-442b-88b1-67d8c3b10f68",
        "created_at": "2010-01-13T19:46:49.747837",
        "updated_at": None,
    }
)


def test_get_user(test_app):
    async def mock_get_current_user():
        return TEST_USER

    app.dependency_overrides[get_current_user] = mock_get_current_user

    resp = test_app.get("/api/user/me")
    print(json.dumps(resp.json(), indent=4))
    assert resp.status_code == 200
    assert resp.json() == jsonable_encoder(
        TEST_USER
    )  # Best way to convert uuid/datetime is to add validator


def test_update_user(test_app, monkeypatch):
    test_request_payload = {
        "username": "updated_user",
        "email": "updated_email@gmail.com",
    }
    test_updated_user = UserOut(**{**TEST_USER.dict(), **test_request_payload})

    async def mock_get_current_user():
        return TEST_USER

    async def mock_update_user(session, redis_conn, current_user_id, data):
        return test_updated_user

    monkeypatch.setattr(user, "update_user", mock_update_user)

    app.dependency_overrides[get_current_user] = mock_get_current_user

    resp = test_app.put("/api/user/me", json=test_request_payload)
    print(json.dumps(resp.json(), indent=4))
    assert resp.status_code == 200
    assert resp.json() == jsonable_encoder(test_updated_user)


def test_delete_user(test_app, monkeypatch):
    async def mock_get_current_user():
        return TEST_USER

    async def mock_delete_user(session, redis_conn, current_user_id):
        return None

    monkeypatch.setattr(user, "delete_user", mock_delete_user)

    app.dependency_overrides[get_current_user] = mock_get_current_user

    resp = test_app.delete("/api/user/me")
    assert resp.status_code == 204
