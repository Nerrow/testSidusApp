from app.api import auth
from app.main import app


def test_signin_success(test_app, monkeypatch, fastapi_dep):
    with fastapi_dep(app).override(
        {"get_postgres_session": lambda: print("Override pg")}
    ):
        test_request_payload = {"email": "test@mail.com", "password": "testpassword"}
        test_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0NzZlMzg2Yy01NjIyLTQ0MmItODhiMS02N2Q4YzNiMTBmNjgiLCJleHAiOjE2NzIxNzA0MTB9.t4F5J3qIhb2vAQFsoTBJEwDyUhcabk6vk-NSGeWr1iw"
        test_response_payload = {"token": test_access_token}

        async def mock_signin(session, payload):
            return test_access_token

        monkeypatch.setattr(auth, "signin", mock_signin)

        resp = test_app.post("/api/auth/signin", json=test_request_payload)
        assert resp.status_code == 200
        assert resp.json() == test_response_payload


def test_signup_success(test_app, monkeypatch, fastapi_dep):
    with fastapi_dep(app).override(
        {"get_postgres_session": lambda: print("Override pg")}
    ):
        test_request_payload = {
            "email": "test@mail.com",
            "password": "testpassword",
            "username": "test_username",
        }
        test_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0NzZlMzg2Yy01NjIyLTQ0MmItODhiMS02N2Q4YzNiMTBmNjgiLCJleHAiOjE2NzIxNzA0MTB9.t4F5J3qIhb2vAQFsoTBJEwDyUhcabk6vk-NSGeWr1iw"
        test_response_payload = {"token": test_access_token}

        async def mock_signup(session, payload):
            return test_access_token

        monkeypatch.setattr(auth, "signup", mock_signup)

        resp = test_app.post("/api/auth/signup", json=test_request_payload)
        assert resp.status_code == 200
        assert resp.json() == test_response_payload
