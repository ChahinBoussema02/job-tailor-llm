# Job Tailor LLM (Resume + Job Description → Tailored Output) ✅

A **portfolio-ready FastAPI LLM project** that takes a **resume + job description** and generates:

- a tailored professional summary
- improved resume bullets
- a short cover letter draft
- keyword matching (matched vs missing)

Built for **real-world job applications** and designed with a **clean API contract + tests**.

---

## ✨ What this service does

You send:

- `resume_text`
- `job_text`
- `target_role`

It returns:

✅ `summary`  
✅ `resume_bullets`  
✅ `cover_letter`  
✅ `keywords` (matched/missing + match score)  
✅ `debug.latency_ms`

---

## 🔧 Tech Stack

- **FastAPI** (REST API)
- **Ollama** (local LLM runtime)
- **Pytest** (API contract tests)
- **Pydantic** (request/response validation)
- **Docker + docker-compose** (optional)

---

## 📦 Project Structure

```bash
job-tailor-llm/
  app/
    main.py              # FastAPI app + /tailor endpoint
    prompts.py           # prompt templates (system/user)
    keywords.py          # keyword match logic
    ollama_client.py     # Ollama chat call helper
    schemas.py           # Pydantic request/response models
  tests/
    test_api_shape.py        # output shape tests
    test_api_contract.py     # contract + error behavior tests
  Dockerfile
  docker-compose.yml
  requirements.txt
  README.md
```

---

## 🚀 Quickstart (Local)

### 1) Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run the API

```bash
uvicorn app.main:app --reload
```

Open docs:

- http://127.0.0.1:8000/docs

---

## 🦙 Ollama Setup (Local LLM)

Install Ollama:

- https://ollama.com

Pull a model (example):

```bash
ollama pull llama3.2:3b
```

Then set your environment variables:

```bash
export OLLAMA_HOST=http://localhost:11434
export OLLAMA_MODEL=llama3.2:3b
```

---

## ✅ Example Request (POST /tailor)

### curl

```bash
curl -sS -X POST "http://127.0.0.1:8000/tailor" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Software engineer experienced with Python and FastAPI. Built internal APIs, wrote unit tests with pytest, and deployed services using Docker. Worked closely with product teams and improved API latency by optimizing database queries.",
    "job_text": "Looking for a Python engineer with FastAPI experience. Must be comfortable writing tests and building REST APIs. Docker knowledge is preferred.",
    "target_role": "Python Backend Engineer"
  }' | jq
```

---

## ✅ Example Response

```json
{
  "summary": "Software engineer with experience in Python and FastAPI, specializing in building and deploying internal APIs. Proven ability to optimize performance and collaborate effectively with product teams.",
  "resume_bullets": [
    "Developed internal APIs using Python and FastAPI.",
    "Wrote unit tests using pytest to ensure code quality and reliability.",
    "Deployed services using Docker, streamlining the development and deployment process.",
    "Collaborated with product teams to deliver high-quality API solutions.",
    "Improved API latency by optimizing database queries, resulting in enhanced performance."
  ],
  "cover_letter": "Dear [Hiring Manager],\n\nI am writing to express my keen interest in the Python Backend Engineer position. My experience with Python and FastAPI aligns perfectly with the requirements outlined in the job description. I have a proven track record of building internal APIs, writing comprehensive unit tests, and deploying services using Docker. I am particularly proud of my ability to optimize database queries, which resulted in significant improvements in API latency. I am eager to contribute my skills and experience to your team.\n\nSincerely,\n[Your Name]",
  "keywords": {
    "matched": [
      "apis",
      "docker",
      "engineer",
      "fastapi",
      "python",
      "tests"
    ],
    "missing": [
      "building",
      "comfortable",
      "experience",
      "knowledge",
      "looking",
      "must",
      "preferred",
      "rest",
      "writing"
    ],
    "match_score": 0.4
  },
  "debug": {
    "latency_ms": 71494
  }
}
```

---

## 🧪 Tests

Run all tests:

```bash
pytest -q
```

---

## 🐳 Docker (Optional)

If you want to run the API inside Docker:

```bash
docker compose up --build
```

Then open:

- http://127.0.0.1:8000/docs

---

## ⚠️ Notes / Limitations

This is a portfolio prototype:

- output quality depends on your local Ollama model
- no database (stateless API)
- keyword matching is basic string matching (not embeddings)

---

## ✅ Next Improvements (Roadmap)

Ideas to upgrade this into a stronger “real product” project:

- add streaming generation (`/tailor/stream`)
- add PDF resume parsing
- add a mini frontend UI (upload resume + job posting)
- improve keyword matching with embeddings + weighting
- export results as `.docx` or `.pdf`
