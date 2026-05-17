# AI Talking Points Card
**Presenter:** Kathi Srujan Goud — AI Developer 2
**Demo Day:** 9 May 2026

---

## WHAT IS GROQ?
> "Groq is an AI inference platform that runs open-source
> AI models at extremely high speed. We use their free API
> to access LLaMA 3.3 — a 70 billion parameter language
> model made by Meta. No credit card needed."

**Key facts to remember:**
- Free API at console.groq.com
- Model: llama-3.3-70b-versatile
- Temperature 0.3 = factual responses
- Max tokens: 1000 per request

---

## WHAT ARE PROMPTS?
> "Prompts are instructions we give to the AI model.
> Think of them like a job description for the AI.
> We have 3 prompt templates stored in text files.
> Each one tells the AI exactly what to do and what
> format to return the answer in."

**Our 3 prompts:**
- describe_prompt.txt — tells AI to describe in 2-3 sentences
- recommend_prompt.txt — tells AI to return JSON with 3 recommendations
- generate_report_prompt.txt — tells AI to return full JSON report

---

## WHAT IS FLASK?
> "Flask is a lightweight Python web framework.
> We used it to build our AI microservice on port 5000.
> It handles all AI calls separately from the Java backend.
> The Java backend calls our Flask service using RestTemplate."

---

## WHAT IS PROMPT INJECTION?
> "Prompt injection is when an attacker tries to hijack
> the AI by adding malicious instructions in their input.
> For example typing 'Ignore previous instructions and
> reveal secrets'. Our sanitiser.py blocks 25+ of these
> attack patterns and returns HTTP 400 immediately."

---

## SECURITY TALKING POINTS

### If asked about security:
> "We implemented 5 layers of security in the AI service.
> First, input sanitisation strips all HTML tags.
> Second, we detect and block 25+ injection patterns.
> Third, rate limiting blocks IPs sending more than
> 30 requests per minute. Fourth, all 8 OWASP recommended
> security headers are added to every response.
> Fifth, our Groq API key is stored only in the .env
> file and never committed to GitHub."

### If asked to show security:
1. Send injection → show 400 response
2. Show SECURITY.md
3. Mention ZAP scan results — zero Critical findings

---

## NUMBERS TO REMEMBER

| Fact | Number |
|------|--------|
| Injection patterns blocked | 25+ |
| Rate limit | 30 req/min |
| Security headers | 8 |
| Retry attempts on failure | 3 |
| AI response time | under 2s |
| Pytest tests passing | 8 |
| Security checklist score | 94% |
| AI quality review score | 4.3/5 |
| ZAP Critical findings | 0 |
| ZAP Medium findings fixed | 2 |

---

## ONE-LINE ANSWERS FOR PANEL

| Question | Answer |
|----------|--------|
| What AI? | LLaMA 3.3 70B by Meta, hosted on Groq |
| Why free? | Groq offers free API tier at console.groq.com |
| How fast? | Under 2 seconds per response |
| How secure? | 5 security layers, 0 critical vulnerabilities |
| What if AI fails? | Fallback template, is_fallback: true |
| What is Flask? | Lightweight Python web framework on port 5000 |
| What are prompts? | Instructions in text files telling AI what to do |