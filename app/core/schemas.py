from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class TailorRequest(BaseModel):
    resume_text: str = Field(..., min_length=1)
    job_text: str = Field(..., min_length=1)
    target_role: str = Field(..., min_length=1)

class KeywordsOut(BaseModel):
    matched: List[str]
    missing: List[str]
    match_score : float = Field(..., ge = 0.0, le = 1.0)

class TailorResponse(BaseModel):
    summary: str
    resume_bullets: List[str]
    cover_letter: str
    keywords: KeywordsOut
    debug: Dict[str, Any] = {}