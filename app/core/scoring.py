import re
from typing import List, Tuple, Set

_STOP = {
    "the","a","an","and","or","to","for","of","in","on","with","is","are","was","were",
    "this","that","it","as","by","from","at","be","will","can","you","we","i"
}

def _tokens(text: str) -> Set[str]:
    toks = re.findall(r"[a-z0-9]+", (text or "").lower())
    return {t for t in toks if len(t) >= 4 and t not in _STOP}

def keyword_match(resume_text: str, job_text: str) -> Tuple[List[str], List[str], float]:
    r = _tokens(resume_text)
    j = _tokens(job_text)
    if not j:
        return [], [], 0.0
    
    matched = sorted(list(r & j))
    missing = sorted(list(j - r))

    score = len(matched) / max(1, len(j))
    return matched[:30], missing[:30], float(min(1.0, max(0.0, score)))

