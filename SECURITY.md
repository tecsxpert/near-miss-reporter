# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please send an e-mail to security@nearmissreporter.local.

We consider the following to be critical vulnerabilities:
- SQL Injection
- Cross-Site Scripting (XSS)
- Authentication Bypass (e.g., 401 without token)
- Unauthorized Data Access

## Security Features Implemented
- **Authentication**: Basic custom authentication matching username/password with database records.
- **Headers**: CORS policy configured globally via `@CrossOrigin` in Spring Boot controllers.
- **Input Validation**: Prepared statements (JPA/Hibernate) prevent SQL injection. Basic payload inspection prevents common XSS and SQLi payloads.
