# 🚨 Near-Miss Reporter

> A full-stack workplace safety application for reporting, tracking, and analyzing near-miss incidents with AI-powered insights.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development Setup](#local-development-setup)
  - [Docker Deployment](#docker-deployment)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Security](#security)
- [License](#license)

---

## Overview

**Near-Miss Reporter** is an enterprise-grade incident reporting platform designed to help organizations capture, manage, and learn from near-miss events before they escalate into actual accidents. The system combines a modern React dashboard with a robust Spring Boot backend and an AI-powered analysis service to deliver actionable safety insights in real time.

---

## Features

### Core Reporting
- **Create / Update / Delete** near-miss reports with title, description, severity, location, and status
- **Soft-delete** mechanism ensures data is never permanently lost
- **Paginated listing** and **full-text search** across reports

### Data Import & Export
- **CSV Import** — bulk-upload historical incidents via file upload (with type & size validation, max 5 MB)
- **CSV Export** — download all report data as a `.csv` file for offline analysis

### Analytics Dashboard
- Interactive charts powered by **Recharts** (severity distribution, status breakdown, trend lines)
- KPI cards with real-time counts

### AI-Powered Insights
- Integrated **Groq LLaMA 3.3 70B** model for natural-language analysis
- `/describe` — generates a human-readable summary of incident data
- `/recommend` — produces actionable safety recommendations
- `/report` — creates a structured safety report from raw data

### Email Notifications
- Automated **HTML email alerts** on every Create, Update, and Delete action via Spring Mail + Gmail SMTP

### Audit Logging
- **Spring AOP** aspect automatically logs every `CREATE`, `UPDATE`, and `DELETE` operation to an `audit_log` table with timestamps and user info

### Authentication
- User registration and login
- Protected routes on the frontend via React Context + `PrivateRoute` wrapper
- Token-based request interceptor (Axios)

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 19, Vite 8, React Router 7, Recharts, TailwindCSS 3, Axios, React Hot Toast, React Icons |
| **Backend** | Java 17, Spring Boot 3.2.5, Spring Data JPA, Spring Mail, Spring AOP, Flyway |
| **AI Service** | Python 3, Flask, Groq API (LLaMA 3.3 70B Versatile) |
| **Database** | PostgreSQL 15 |
| **API Docs** | SpringDoc OpenAPI (Swagger UI) |
| **DevOps** | Docker, Docker Compose |

---

## Architecture

```
┌──────────────┐       ┌──────────────────┐       ┌─────────────────┐
│   Frontend   │──────▶│   Backend (API)  │──────▶│  PostgreSQL 15  │
│  React/Vite  │  HTTP │  Spring Boot     │  JPA  │                 │
│  Port 5173   │       │  Port 8080       │       │  Port 5432      │
└──────────────┘       └────────┬─────────┘       └─────────────────┘
                                │
                                │  Email (SMTP)
                                ▼
                       ┌──────────────────┐
                       │   Gmail SMTP     │
                       └──────────────────┘

┌──────────────┐
│  AI Service  │  ◀── Groq Cloud API (LLaMA 3.3 70B)
│  Flask       │
│  Port 5000   │
└──────────────┘
```

---

## Getting Started

### Prerequisites

| Tool | Version |
|---|---|
| Java | 17+ |
| Node.js | 18+ |
| Python | 3.9+ |
| PostgreSQL | 15+ |
| Maven | 3.8+ (or use the included `mvnw` wrapper) |
| Docker *(optional)* | 20+ |

### Local Development Setup

#### 1. Clone the repository

```bash
git clone https://github.com/your-username/near-miss-reporter.git
cd near-miss-reporter
```

#### 2. Database

Create a PostgreSQL database:

```sql
CREATE DATABASE near_miss;
```

#### 3. Backend

```bash
cd backend

# Configure database credentials in src/main/resources/application.properties
# spring.datasource.url=jdbc:postgresql://localhost:5432/near_miss
# spring.datasource.username=postgres
# spring.datasource.password=<your-password>

# Run the application (Flyway will auto-migrate the schema)
./mvnw spring-boot:run
```

The backend starts at **http://localhost:8080**.  
Swagger UI is available at **http://localhost:8080/swagger-ui.html**.

#### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend starts at **http://localhost:5173**.

#### 5. AI Service

```bash
cd ai-service

# Create a .env file with your Groq API key
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

pip install -r requirements.txt
python app.py
```

The AI service starts at **http://localhost:5000**.

### Docker Deployment

Spin up the entire stack with a single command:

```bash
# Set the Groq API key in your environment
export GROQ_API_KEY=your_groq_api_key_here

docker-compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:80 |
| Backend API | http://localhost:8080 |
| AI Service | http://localhost:5000 |
| PostgreSQL | localhost:5432 |

---

## API Reference

### Auth Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Login with username & password |

### Report Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/add` | Create a new report |
| `GET` | `/api/page?page=0&size=5` | Get paginated reports (excludes soft-deleted) |
| `GET` | `/api/search?q=keyword&page=0&size=5` | Search reports by title or description |
| `PUT` | `/api/update/{id}` | Update an existing report |
| `DELETE` | `/api/delete/{id}` | Soft-delete a report |

### File & Export Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/upload` | Upload a file (CSV import / image / PDF) |
| `GET` | `/api/export` | Export all reports as CSV |

### AI Service Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/describe` | Generate AI-powered incident description |
| `POST` | `/recommend` | Get AI safety recommendations |
| `POST` | `/report` | Generate a structured safety report |
| `GET` | `/health` | Health check with uptime & model info |

---

## Project Structure

```
near-miss-reporter/
├── backend/                        # Spring Boot API
│   ├── src/main/java/.../
│   │   ├── controller/
│   │   │   ├── AuthController.java       # Login & Registration
│   │   │   ├── ReportController.java     # CRUD + Search + Pagination
│   │   │   ├── FileUploadController.java # CSV Import & File Upload
│   │   │   └── ExportController.java     # CSV Export
│   │   ├── entity/
│   │   │   ├── Report.java               # Report data model
│   │   │   ├── User.java                 # User data model
│   │   │   └── AuditLog.java             # Audit trail model
│   │   ├── repository/                   # Spring Data JPA repos
│   │   ├── service/
│   │   │   ├── ReportService.java        # Business logic
│   │   │   ├── EmailService.java         # HTML email notifications
│   │   │   └── AuditLoggingAspect.java   # AOP audit logging
│   │   ├── config/                       # CORS, security config
│   │   └── exception/                    # Global error handling
│   ├── src/main/resources/
│   │   └── application.properties        # DB, mail, flyway config
│   ├── Dockerfile
│   └── pom.xml
│
├── frontend/                       # React + Vite SPA
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx                  # Dashboard with report list
│   │   │   ├── Analytics.jsx             # Charts & KPI dashboard
│   │   │   ├── ReportDetail.jsx          # Single report view
│   │   │   ├── Login.jsx                 # Login page
│   │   │   └── Register.jsx              # Registration page
│   │   ├── components/
│   │   │   └── AuthContext.jsx           # Auth state management
│   │   ├── services/
│   │   │   └── api.js                    # Axios instance + interceptors
│   │   ├── App.jsx                       # Routes & PrivateRoute guard
│   │   └── main.jsx                      # Entry point
│   ├── Dockerfile
│   └── package.json
│
├── ai-service/                     # Python Flask AI microservice
│   ├── app.py                            # Flask app + security headers
│   ├── routes/                           # Describe, Recommend, Report
│   ├── services/                         # Groq API integration
│   ├── prompts/                          # AI prompt templates
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml              # Full-stack orchestration
├── sample_reports.csv              # Sample data for CSV import demo
├── demo_scenarios.md               # Demo walkthrough scripts
├── SECURITY.md                     # Security policy & vulnerability reporting
├── .env.example                    # Environment variable template
└── README.md                       # ← You are here
```

---

## Security

- **Input Validation** — XSS (`<script>`) and SQL injection (`OR 1=1`) payloads are blocked at the controller level
- **Prepared Statements** — Spring Data JPA parameterized queries prevent SQL injection
- **Security Headers** — `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Strict-Transport-Security`, and `Content-Security-Policy` headers on the AI service
- **Audit Trail** — Every data mutation is logged via Spring AOP to the `audit_log` table
- **Soft Deletes** — Reports are never physically removed from the database

For vulnerability reporting, see [SECURITY.md](SECURITY.md).

---

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | API key for Groq cloud AI service | Yes (AI service) |
| `SPRING_DATASOURCE_URL` | JDBC URL for PostgreSQL | Yes (backend) |
| `SPRING_DATASOURCE_USERNAME` | Database username | Yes (backend) |
| `SPRING_DATASOURCE_PASSWORD` | Database password | Yes (backend) |

