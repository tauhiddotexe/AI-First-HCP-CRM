# API Specification

# AI-First CRM – HCP Interaction Logger

Version: 1.0

---

# 1. Overview

This document defines the REST API specification for the AI-First CRM application.

The API follows RESTful conventions and serves as the communication layer between the React frontend and the FastAPI backend.

All endpoints return JSON.

Base URL

/api/v1

---

# 2. API Design Principles

- RESTful endpoints
- JSON request/response
- UUID identifiers
- Consistent error responses
- Versioned API
- Strong validation using Pydantic
- Stateless requests

---

# 3. Authentication

(Currently simplified for assignment.)

Future support:

- JWT
- OAuth2
- Role-Based Access Control (RBAC)

Authorization Header

Bearer <token>

---

# 4. Standard Response Format

## Success

```json
{
    "success": true,
    "message": "Interaction logged successfully.",
    "data": {}
}
```

## Error

```json
{
    "success": false,
    "message": "Validation failed.",
    "errors": [
        {
            "field": "interaction_date",
            "message": "Date is required."
        }
    ]
}
```

---

# 5. Health Check

## GET /health

Purpose

Verify API availability.

Response

```json
{
    "status": "healthy"
}
```

---

# 6. HCP APIs

---

## GET /hcps

Returns all HCPs.

Response

```json
[
    {
        "id":"...",
        "name":"Dr. Sarah Patel",
        "specialization":"Cardiology"
    }
]
```

---

## GET /hcps/{hcp_id}

Returns complete HCP information.

---

## POST /hcps

Creates new HCP.

Request

```json
{
    "first_name":"Sarah",
    "last_name":"Patel",
    "specialization":"Cardiology",
    "hospital":"City Hospital"
}
```

---

## PATCH /hcps/{hcp_id}

Updates HCP.

---

# 7. Interaction APIs

---

## POST /interactions

Creates interaction.

Request

```json
{
    "hcp_id":"uuid",
    "interaction_type":"Face-to-Face",
    "interaction_date":"2026-07-08",
    "summary":"..."
}
```

Response

```json
{
    "id":"uuid",
    "status":"created"
}
```

---

## GET /interactions

Returns interaction list.

Supports

- Pagination
- Sorting
- Filters

Query Parameters

page

limit

hcp

date

---

## GET /interactions/{id}

Returns one interaction.

---

## PATCH /interactions/{id}

Updates interaction.

Only modified fields should be updated.

---

## DELETE /interactions/{id}

Soft delete.

---

# 8. AI Chat API

## POST /agent/chat

Primary endpoint used by frontend.

This endpoint invokes LangGraph.

Request

```json
{
    "message":"Today I met Dr. Shah...",
    "interaction_id":null
}
```

Response

```json
{
    "assistant_message":"I've logged your interaction.",
    "tool_used":"LogInteraction",
    "updated_form":{

    },
    "interaction_id":"uuid"
}
```

---

# 9. LangGraph Tool API

Although tools are internal, each tool should expose a service interface.

---

## Log Interaction

POST

/tools/log-interaction

Input

Natural language

Output

Structured interaction

---

## Edit Interaction

PATCH

/tools/edit-interaction

---

## Retrieve History

GET

/tools/history/{hcp_id}

---

## Next Best Action

POST

/tools/next-action

---

## Visit Summary

POST

/tools/summary

---

# 10. Chat History

## GET /chat/{interaction_id}

Returns conversation history.

Response

```json
[
    {
        "role":"user",
        "message":"..."
    },
    {
        "role":"assistant",
        "message":"..."
    }
]
```

---

# 11. Follow-Up APIs

## GET /followups

Returns pending follow-ups.

---

## POST /followups

Creates follow-up.

---

## PATCH /followups/{id}

Updates follow-up.

---

# 12. Dashboard APIs

## GET /dashboard

Returns CRM metrics.

Example

```json
{
    "total_interactions":124,
    "pending_followups":15,
    "hcp_count":42
}
```

---

# 13. Validation Rules

Interaction

Required

- HCP
- Date
- Interaction Type

Optional

- Summary
- Materials
- Samples
- Outcome
- Sentiment

Maximum message size

5000 characters

---

# 14. Status Codes

200

Success

201

Created

400

Validation Error

401

Unauthorized

403

Forbidden

404

Not Found

409

Conflict

422

Invalid Request

500

Internal Server Error

---

# 15. Pagination

Standard format

```json
{
    "items":[...],
    "page":1,
    "limit":20,
    "total":142,
    "pages":8
}
```

---

# 16. Filtering

Interactions support

- HCP
- Date Range
- Interaction Type
- Representative
- Sentiment

Example

GET

/interactions?hcp=uuid&type=Virtual

---

# 17. Future APIs

Analytics

Notifications

Calendar

Voice Notes

Email

CRM Export

Medical Insights

---

# 18. API Flow

Frontend

↓

Redux

↓

API Client

↓

FastAPI

↓

Service Layer

↓

LangGraph

↓

Tool

↓

Database

↓

Response

↓

Redux

↓

UI

---

# 19. Design Principles

- Consistent responses
- Thin controllers
- Typed schemas
- Stateless endpoints
- Easy integration
- Extensible routes
- Clear separation between AI endpoints and CRUD endpoints

---

# 20. Summary

The API exposes REST endpoints for managing HCPs, interactions, follow-ups, chat conversations, and dashboard data while delegating AI reasoning to the LangGraph orchestration layer. The frontend communicates exclusively through these APIs, ensuring a clean separation between presentation, business logic, and AI workflows.