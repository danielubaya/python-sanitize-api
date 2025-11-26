from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_uses_app_banned_words_txt():
    res = client.post("/sanitize", json={"text": "Foo and bar"})
    assert res.status_code == 200
    assert res.json()["cleaned"] == "F*o and b*r"
