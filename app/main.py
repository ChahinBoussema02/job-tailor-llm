from dotenv import load_dotenv
load_dotenv()

import time
from fastapi import FastAPI, HTTPException

from app.core.schemas import TailorRequest, TailorResponse, KeywordsOut
from app.core.prompts import SYSTEM_PROMPT, build_user_prompt
from app.core.llm import call_ollama_chat
from app.core .scoring import keyword_match

app = FastAPI(title = "Job Tailor LLM")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/tailor", response_model = TailorResponse)
def tailor(req: TailorRequest):
    if len(req.resume_text.strip()) < 50 or len(req.job_text.strip()) < 50:
        raise HTTPException(
            status_code=400,
            detail="resume_text and job_text must be at least 50 characters."
        )
    t0 = time.perf_counter()

    matched, missing, score = keyword_match(req.resume_text, req.job_text)

    user_prompt = build_user_prompt(req.resume_text, req.job_text, req.target_role)

    try:
        data = call_ollama_chat(SYSTEM_PROMPT, user_prompt)
    except Exception as e:
        raise HTTPException(status_code = 502, detail = f"LLM error: {e.__class__.__name__}")
    
    # Basic validation/guardrails
    summary = str(data.get("summary", "")).strip()
    bullets = data.get("resume_bullets", [])
    cover = str(data.get("cover_letter", "")).strip()

    if not summary or not isinstance(bullets, list) or not cover:
        raise HTTPException(status_code = 500, detail = "Model returned invalid JSON shape")
    
    #Use deterministic keyword score (so tests are stable)
    out = TailorResponse(
        summary=summary,
        resume_bullets=[str(x).strip() for x in bullets if str(x).strip()][:12],
        cover_letter=cover,
        keywords=KeywordsOut(matched=matched, missing=missing, match_score=score),
        debug={"latency_ms": int((time.perf_counter() - t0) * 1000)},
    )
    return out