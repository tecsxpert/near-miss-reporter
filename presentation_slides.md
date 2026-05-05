---
title: Near-Miss Reporter
subtitle: Intelligent Safety Management
theme: default
---

# Slide 1: The Problem & Our Solution

### The Problem
- **Under-reporting**: Near-misses often go unreported due to complex, paper-based forms.
- **Lack of Actionable Insights**: Data sits in silos; patterns leading to critical accidents are missed.
- **Compliance Gaps**: Poor auditing and lack of secure data trails.

### Our Solution
- A **frictionless**, mobile-responsive React dashboard to log incidents in seconds.
- **AI-Powered Insights** that analyze reports to suggest preventative safety measures instantly.
- **Enterprise-Grade Backend** with Spring Boot, ensuring secure, audited, and reliable data storage.

---

# Slide 2: Architecture & Tech Stack

### Frontend (User Experience)
- **Vite + React**: Lightning-fast UI.
- **Tailwind CSS**: Fully responsive design (Mobile to Desktop).
- **Recharts**: Dynamic visual analytics.

### Backend (The Core Engine)
- **Spring Boot 3 (Java 17)**: RESTful API, AOP for Audit Logging.
- **PostgreSQL + Flyway**: Robust data persistence and versioned schema migrations.
- **Security**: Token-based authentication, strict input sanitization.

### AI Service (The Brain)
- **Python / Flask**: Lightweight microservice.
- **Llama 3 via Groq API**: Generates real-time safety recommendations.

---

# Slide 3: Demo Flow

### What You Will See Today:
1. **Frictionless Reporting**: Submitting an incident and viewing real-time KPI updates.
2. **AI in Action**: Requesting AI recommendations based on the current dashboard data.
3. **Data Ingestion & Analytics**: Importing bulk legacy data (CSV) and analyzing trends.
4. **Security & Audit**: Demonstrating robust injection protection and our silent audit trail.

*Let's jump into the live system!*
