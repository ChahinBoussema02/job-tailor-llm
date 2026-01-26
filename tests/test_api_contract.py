import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_tailor_short_input_still_works(monkeypatch):
    # keep tests deterministic + fast (no real Ollama call)
    def fake_call(system_prompt: str, user_prompt: str):
        return {
            "summary": "Backend engineer with Python/FastAPI.",
            "resume_bullets": ["Built FastAPI services.", "Wrote tests."],
            "cover_letter": "I’m excited to apply.",
            "keywords": {"matched": [], "missing": [], "match_score": 0.0},
        }

    monkeypatch.setattr("app.main.call_ollama_chat", fake_call)

    payload = {
        "resume_text": ("Python FastAPI backend APIs. Tests. " * 3),  # > 50 chars
        "job_text": ("Need FastAPI engineer for API development. " * 3),  # > 50 chars
        "target_role": "Backend Engineer",
    }

    r = client.post("/tailor", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()

    assert isinstance(data["summary"], str) and data["summary"]
    assert isinstance(data["resume_bullets"], list) and len(data["resume_bullets"]) >= 1
    assert isinstance(data["cover_letter"], str) and data["cover_letter"]
    assert "keywords" in data and isinstance(data["keywords"], dict)


def test_tailor_missing_fields_returns_422():
    # FastAPI/Pydantic should reject bad payloads
    r = client.post("/tailor", json={"resume_text": "only this"})
    assert r.status_code == 422


def test_tailor_llm_failure_returns_502(monkeypatch):
    def boom(system_prompt: str, user_prompt: str):
        raise RuntimeError("ollama down")

    monkeypatch.setattr("app.main.call_ollama_chat", boom)

    payload = {
        "resume_text": ("Python FastAPI backend APIs. Tests. " * 3),   # > 50 chars
        "job_text": ("Need FastAPI engineer for API development. " * 3), # > 50 chars
        "target_role": "Backend Engineer",
    }

    r = client.post("/tailor", json=payload)
    assert r.status_code == 502, r.text