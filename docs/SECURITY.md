# Security Guidelines

# AI-First CRM – HCP Interaction Logger

Version: 1.0

---

# 1. Purpose

This document defines the security architecture and implementation guidelines for the AI-First CRM application.

Although this is an interview assignment, the application should demonstrate production-oriented security practices where practical without adding unnecessary complexity.

Security should be considered throughout the application rather than treated as a final step.

---

# 2. Security Goals

The application should:

- Protect sensitive credentials
- Prevent unauthorized access
- Validate all user input
- Secure AI interactions
- Protect database integrity
- Prevent common web vulnerabilities
- Follow the principle of least privilege

---

# 3. Threat Model

Primary attack surfaces include:

- REST API
- AI Chat Interface
- LangGraph Tools
- Database
- Environment Variables
- Docker Configuration

---

# 4. Authentication

Assignment Scope

The application uses a single demo Sales Representative account.

Implementation Requirements

- No credentials stored in frontend
- Demo user created server-side
- Authentication layer designed for future JWT integration
- Never trust client identity

Future

- JWT Authentication
- OAuth2
- Role-Based Access Control (RBAC)

---

# 5. Authorization

Even with a demo user, backend APIs must never trust user-supplied IDs.

Rules

- Backend determines current user
- Ignore client-provided ownership information
- Prevent access to interactions owned by other users
- Validate permissions before executing LangGraph tools

---

# 6. Secrets Management

Never commit:

- API Keys
- Database Passwords
- Tokens
- Secrets

Store all sensitive configuration in environment variables.

Required

.env.example

Never commit

.env

Never expose secrets to frontend.

---

# 7. API Security

Every request should be validated.

Use:

- Pydantic validation
- Request schema validation
- Response schema validation

Reject:

- Invalid UUIDs
- Invalid dates
- Empty required fields
- Malformed JSON

---

# 8. Input Validation

Validate all user input.

Examples

- HCP names
- Dates
- Chat messages
- Notes
- IDs

Maximum chat message length

5000 characters

Reject oversized payloads.

---

# 9. SQL Injection Protection

Use SQLAlchemy ORM.

Never concatenate SQL strings.

Always use parameterized queries.

---

# 10. XSS Protection

Never render raw HTML from AI responses.

Render AI responses as escaped plain text.

Sanitize any future Markdown rendering.

---

# 11. CSRF

Current architecture uses JSON APIs.

If cookie authentication is introduced in the future, enable CSRF protection.

---

# 12. CORS

Allow only trusted frontend origins.

Development

http://localhost:3000

or

http://localhost:5173

Production

Explicit frontend domain only.

Never use

Access-Control-Allow-Origin: *

in production.

---

# 13. Environment Variables

Required

GROQ_API_KEY

DATABASE_URL

POSTGRES_USER

POSTGRES_PASSWORD

POSTGRES_DB

Never expose backend secrets through Vite.

Only variables prefixed with

VITE_

should reach the frontend.

---

# 14. AI Security

The LangGraph agent must never directly execute arbitrary user instructions.

User input should only influence:

- Entity extraction
- Intent detection
- Tool selection

Never allow prompts to:

- Execute code
- Read files
- Access environment variables
- Execute shell commands
- Modify application configuration

---

# 15. Prompt Injection Protection

Treat every user message as untrusted.

System prompts must always remain authoritative.

The LLM should ignore requests attempting to:

- Reveal system prompts
- Reveal API keys
- Ignore previous instructions
- Change internal behavior
- Access hidden application state

---

# 16. LangGraph Tool Security

Every tool should validate:

- Required parameters
- Entity ownership
- Database existence

Tools must never trust LLM output without validation.

LLM output should be considered untrusted until validated.

---

# 17. Database Security

Application database user should have only required permissions.

Avoid:

- Superuser privileges
- DROP permissions
- Database administration rights

Use least privilege.

---

# 18. Logging

Never log:

- API Keys
- Tokens
- Passwords
- Database credentials
- Full chat history containing sensitive information

Log only:

- Request IDs
- Endpoint
- Processing time
- Tool executed
- Success/Failure

---

# 19. Error Handling

Never expose:

- Stack traces
- SQL errors
- Internal exceptions
- File paths
- Environment variables

Users should receive friendly error messages.

Detailed errors belong only in server logs.

---

# 20. Docker Security

Do not include:

- Secrets in Docker images
- Hardcoded credentials
- Development .env files

Use environment variables through Docker Compose.

---

# 21. Dependency Security

Keep dependencies updated.

Remove unused packages.

Pin dependency versions where appropriate.

Run vulnerability scans before submission.

---

# 22. HTTP Security Headers

Recommended headers

- X-Content-Type-Options
- X-Frame-Options
- Referrer-Policy
- Content-Security-Policy
- Permissions-Policy

These should be configured through FastAPI middleware.

---

# 23. Rate Limiting

Protect AI endpoints.

Recommended limits

- Chat endpoint
- Interaction creation
- Edit requests

Future implementation may use Redis.

For this assignment, document the strategy even if full implementation is deferred.

---

# 24. Data Protection

Sensitive information should remain server-side.

Do not expose:

- API Keys
- Database credentials
- Internal prompts
- Hidden metadata

Use HTTPS in production.

---

# 25. Audit Logging

Important actions should generate audit records.

Examples

- Interaction Created
- Interaction Edited
- Follow-up Added
- Tool Executed

Store

Timestamp

User

Action

Target Resource

---

# 26. Backup Strategy

Future production deployment should include:

- Automated PostgreSQL backups
- Restore testing
- Disaster recovery procedures

Out of scope for this assignment.

---

# 27. Monitoring

Future production deployment may include:

- API metrics
- Error monitoring
- AI latency
- Database performance
- Tool execution metrics

Out of scope for this assignment.

---

# 28. Security Checklist

Before submission verify:

✓ No hardcoded API keys

✓ No committed .env files

✓ Environment variables configured

✓ SQLAlchemy parameterized queries

✓ Input validation implemented

✓ CORS configured

✓ No secrets exposed to frontend

✓ AI output validated

✓ LangGraph tools validate input

✓ Friendly error messages

✓ Docker contains no secrets

✓ Dependencies reviewed

---

# 29. Out of Scope

The following enterprise features are acknowledged but intentionally excluded due to assignment scope:

- Multi-factor authentication
- OAuth providers
- Production IAM
- WAF
- IDS/IPS
- SIEM integration
- Secrets Manager
- Redis rate limiting
- Multi-tenant isolation
- Kubernetes security
- Cloud infrastructure security

The architecture should allow these to be added later without major redesign.

---

# 30. Summary

Security is implemented using a defense-in-depth approach. The application validates all input, protects secrets through environment variables, restricts backend access, validates AI-generated data before persistence, prevents common web vulnerabilities, and keeps the LangGraph agent isolated from privileged application resources. The design emphasizes secure defaults while remaining appropriate for the scope of an interview assignment.