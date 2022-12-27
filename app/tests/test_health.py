def test_health(test_app):
    resp = test_app.get("/healthcheck")
    assert resp.status_code == 200
    assert resp.json() == {"message": "OK"}
