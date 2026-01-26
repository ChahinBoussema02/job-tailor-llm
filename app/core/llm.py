import json
import os
from typing import Any, Dict

import httpx

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:12b")
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "180"))

def _extract_json(text: str) -> Dict[str, Any]:
    text = (text or "").strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found")
    return json.loads(text[start: end + 1])

def call_ollama_chat(system_prompt: str, user_prompt: str) -> Dict[str, Any]:
    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "options": {"temperature": 0.2, "num_predict": 700},
    }

    r = httpx.post(f"{OLLAMA_HOST}/api/chat", json = payload, timeout = OLLAMA_TIMEOUT)
    r.raise_for_status()
    content = r.json()["message"]["content"]
    return _extract_json(content)