# Near Miss Reporter — AI Service
**Tool-40 | Flask AI Microservice | Port 5000**  
**Developer:** Kathi Srujan Goud — AI Developer 2

---

## Overview
The AI service is a Flask microservice that provides AI-powered
features for the Near Miss Reporter application. It uses Groq's
LLaMA 3.3 70B model to describe incidents, generate recommendations,
and produce full safety reports.

---

## Tech Stack
| Technology | Purpose |
|-----------|---------|
| Python 3.11 | Language |
| Flask 3.0.3 | Web framework |
| Groq API | LLaMA 3.3 70B model |
| flask-limiter | Rate limiting 30 req/min |
| bleach | Input sanitisation |
| pytest | Unit testing |

---

## Endpoints

### GET /health
Check if AI service is running.

**Response:**
```json
{
  "status": "ok",
  "model": "llama-3.3-70b-versatile",
  "generated_at": "2026-05-02T10:00:00"
}
```

---

### POST /describe
Generate a professional description of a near miss incident.

**Request:**
```json
{
  "text": "A worker slipped on a wet floor near the warehouse entrance"
}
```

**Response:**
```json
{
  "description": "A worker experienced a slip incident...",
  "is_fallback": false,
  "generated_at": "2026-05-02T10:00:00"
}
```

---

### POST /recommend
Get 3 safety recommendations for an incident.

**Request:**
```json
{
  "text": "A worker slipped on a wet floor near the warehouse entrance"
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "action_type": "Engineering",
      "description": "Install anti-slip floor mats",
      "priority": "High"
    }
  ],
  "is_fallback": false,
  "generated_at": "2026-05-02T10:00:00"
}
```

---

### POST /generate-report
Generate a full structured safety report.

**Request:**
```json
{
  "text": "A forklift nearly collided with a pedestrian in the loading bay"
}
```

**Response:**
```json
{
  "report": {
    "title": "Forklift Near Miss — Loading Bay",
    "summary": "A near miss incident occurred...",
    "severity": "High",
    "key_items": ["item 1", "item 2"],
    "recommendations": [...]
  },
  "is_fallback": false,
  "generated_at": "2026-05-02T10:00:00"
}
```

---

## Error Responses

| Code | Meaning |
|------|---------|
| 400 | Empty input, missing field, or injection detected |
| 429 | Rate limit exceeded (30 req/min) |
| 500 | Internal server error |

---

## Setup Instructions

### Prerequisites
- Python 3.11+
- Groq API key (free at console.groq.com)

### Step 1 — Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/near-miss-reporter.git
cd near-miss-reporter/ai-service
```

### Step 2 — Create `.env` File
```bash
# In root folder (near-miss-reporter/)
cp .env.example .env
```
Edit `.env` and add your Groq API key:

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the Service
```bash
python app.py
```

Service starts at: **http://localhost:5000**

### Step 5 — Verify Running
```bash
curl http://localhost:5000/health
```

---

## Docker Setup

### Build Image
```bash
docker build -t ai-service .
```

### Run Container
```bash
docker run -p 5000:5000 --env-file ../.env ai-service
```

---

## Running Tests

### All Tests
```bash
pytest test_endpoints.py -v
```

### Security Tests
```bash
python test_security_signoff.py
```

### E2E Tests
```bash
python test_e2e.py
```

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| GROQ_API_KEY | Groq API key from console.groq.com | ✅ Yes |
| AI_SERVICE_URL | URL of this service | No (default: http://localhost:5000) |

---

## Security Features
- ✅ Prompt injection detection (25+ patterns)
- ✅ XSS and command injection blocking
- ✅ Rate limiting — 30 requests per minute
- ✅ Input sanitisation with bleach
- ✅ All 8 OWASP security headers
- ✅ API key stored in .env only
- ✅ 3-retry with exponential backoff
- ✅ Fallback template when AI unavailable

---

## Folder Structure
## Docker Setup
Dockerfile is provided for containerised deployment.
Docker setup requires admin rights on development machine.
To be completed with mentor assistance before production deployment.

### Build Image (when Docker is available)
```bash
docker build -t ai-service .
docker run -p 5000:5000 --env-file ../.env ai-service
```