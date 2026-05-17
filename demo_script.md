# AI Demo Script — Near Miss Reporter
**Presenter:** Kathi Srujan Goud — AI Developer 2  
**Date:** Demo Day — 9 May 2026  
**Time Slot:** 60 seconds for AI explanation  

---

## YOUR 60-SECOND TECH EXPLANATION
*(Memorise this — say it naturally, not robotically)*

> "Our AI service runs on Flask, a Python web framework, on port 5000.
> When a user submits a near miss incident, the text is first sanitised
> to block any prompt injection or XSS attacks. It then gets sent to
> Groq's LLaMA 3.3 70 billion parameter model — which is completely
> free to use. The AI gives us three things: a professional description
> of the incident, three safety recommendations with priority levels,
> and a full structured report. If the AI is unavailable, we have a
> fallback template so the app never crashes. The whole thing responds
> in under 2 seconds."

---

## DEMO SCENARIO 1 — /describe Endpoint

### What to Say
> "Let me show you the AI describing a near miss incident."

### Exact Input to Type