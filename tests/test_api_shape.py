from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_tailor_shape(monkeypatch):
    def fake_call(system_prompt: str, user_prompt: str):
        return {
            "summary": "Backend engineer with Python and FastAPI experience.",
            "resume_bullets": [
                "Built FastAPI services with caching and tests.",
                "Improved API latency by optimizing queries."
            ],
            "cover_letter": "I’m excited to apply. I have relevant experience and enjoy building APIs.",
            "keywords": {"matched": [], "missing": [], "match_score": 0.0}
        }
    
    monkeypatch.setattr("app.main.call_ollama_chat", fake_call)

    payload = {
        "resume_text": "I built FastAPI APIs in Python. I wrote tests and shipped services. " * 3,
        "job_text": "Looking for a Python engineer with FastAPI, testing, and API development." * 3,
        "target_role": "Backend Engineer"
    }

    r = client.post("/tailor", json = payload)
    assert r.status_code == 200, r.text
    data = r.json()

    assert isinstance(data["summary"], str) and data["summary"]
    assert isinstance(data["resume_bullets"], list) and len(data["resume_bullets"]) >= 1
    assert isinstance(data["cover_letter"], str) and data["cover_letter"]
    assert "keywords" in data
    assert 0.0 <= data["keywords"]["match_score"] <= 1.0