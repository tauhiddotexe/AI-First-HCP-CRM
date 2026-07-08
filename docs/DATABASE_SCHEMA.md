# Database Schema

# AI-First CRM – HCP Interaction Logger

Version: 1.0

---

# 1. Purpose

This document defines the relational database schema for the AI-First CRM application.

The database stores structured Healthcare Professional (HCP) information, interaction records, AI-generated summaries, follow-up actions, chat history, and supporting metadata.

The schema is designed to be normalized, scalable, and compatible with PostgreSQL while remaining portable to MySQL.

---

# 2. Design Goals

The schema should prioritize:

- Normalization
- Referential integrity
- Easy querying
- Scalability
- Analytics readiness
- Auditability
- Future CRM integrations

---

# 3. Entity Relationship Overview

User
│
├──────────────┐
│              │
▼              ▼
HCP        ChatMessage
│
│
▼
Interaction
│
├────────────┐
│            │
▼            ▼
Material   FollowUp

---

# 4. Tables

## Users

Stores CRM users.

| Column | Type | Description |
|---------|------|-------------|
| id | UUID | Primary Key |
| full_name | VARCHAR | User name |
| email | VARCHAR | Unique email |
| role | VARCHAR | Sales Rep / Manager |
| created_at | TIMESTAMP | Creation time |
| updated_at | TIMESTAMP | Last update |

---

## HCP

Healthcare Professional master table.

| Column | Type |
|---------|------|
| id | UUID |
| first_name | VARCHAR |
| last_name | VARCHAR |
| title | VARCHAR |
| specialization | VARCHAR |
| hospital | VARCHAR |
| city | VARCHAR |
| phone | VARCHAR |
| email | VARCHAR |
| created_at | TIMESTAMP |

One HCP may have many interactions.

---

## Interaction

Core CRM table.

| Column | Type |
|---------|------|
| id | UUID |
| hcp_id | UUID FK |
| user_id | UUID FK |
| interaction_type | VARCHAR |
| interaction_date | DATE |
| interaction_time | TIME |
| location | VARCHAR |
| summary | TEXT |
| sentiment | VARCHAR |
| outcome | TEXT |
| status | VARCHAR |
| created_at | TIMESTAMP |
| updated_at | TIMESTAMP |

---

## Discussion Topics

Stores multiple discussion topics.

| Column | Type |
|---------|------|
| id | UUID |
| interaction_id | UUID FK |
| topic | TEXT |

Example

- Product efficacy
- Safety
- Pricing
- Competitor comparison

---

## Products Discussed

Stores promoted products.

| Column | Type |
|---------|------|
| id | UUID |
| interaction_id | UUID FK |
| product_name | VARCHAR |

---

## Materials Shared

Stores brochures or educational material.

| Column | Type |
|---------|------|
| id | UUID |
| interaction_id | UUID FK |
| material_name | VARCHAR |
| quantity | INTEGER |

---

## Samples Distributed

Stores pharmaceutical samples.

| Column | Type |
|---------|------|
| id | UUID |
| interaction_id | UUID FK |
| product_name | VARCHAR |
| quantity | INTEGER |

---

## Follow Ups

Tracks future actions.

| Column | Type |
|---------|------|
| id | UUID |
| interaction_id | UUID FK |
| follow_up_date | DATE |
| action | TEXT |
| status | VARCHAR |

Status

- Pending
- Completed
- Cancelled

---

## Chat Messages

Stores AI conversation history.

| Column | Type |
|---------|------|
| id | UUID |
| interaction_id | UUID FK |
| role | VARCHAR |
| message | TEXT |
| created_at | TIMESTAMP |

Role

- User
- Assistant

---

## AI Extraction Log

Stores structured AI output for debugging and auditing.

| Column | Type |
|---------|------|
| id | UUID |
| interaction_id | UUID FK |
| extracted_json | JSONB |
| model | VARCHAR |
| processing_time_ms | INTEGER |
| confidence | DECIMAL |
| created_at | TIMESTAMP |

This table is optional but recommended.

---

# 5. Relationships

Users

1

↓

Many

Interactions

HCP

1

↓

Many

Interactions

Interaction

1

↓

Many

Discussion Topics

Interaction

1

↓

Many

Products

Interaction

1

↓

Many

Materials

Interaction

1

↓

Many

Samples

Interaction

1

↓

Many

FollowUps

Interaction

1

↓

Many

ChatMessages

---

# 6. Constraints

Required

Interaction

- HCP
- Date
- Interaction Type

Optional

- Summary
- Materials
- Samples
- Follow-up
- Sentiment

Foreign keys should enforce referential integrity.

---

# 7. Indexes

Recommended indexes

HCP Name

Interaction Date

User ID

Follow-up Date

Created At

Composite indexes

(hcp_id, interaction_date)

(user_id, interaction_date)

---

# 8. Soft Deletes

Avoid physical deletion.

Every major table should support

deleted_at TIMESTAMP NULL

This enables audit history and recovery.

---

# 9. Audit Fields

Every primary entity should include

created_at

updated_at

created_by

updated_by

This supports enterprise compliance.

---

# 10. Example Interaction

Representative meets Dr. Sarah Patel.

Interaction

↓

Products

- Ozempic

Discussion Topics

- Safety
- Long-term efficacy

Materials

- Product Brochure

Samples

- Ozempic Sample Pack

Follow-up

- Next Tuesday

Chat

Stored separately.

---

# 11. Future Expansion

The schema should support future additions without major changes.

Examples

- Voice recordings
- Calendar events
- Attachments
- Images
- Prescriptions
- Marketing campaigns
- CRM integrations
- Analytics dashboards
- AI recommendations
- Multi-agent workflows

---

# 12. Design Principles

- Normalize data
- Minimize duplication
- Prefer foreign keys
- Keep AI outputs structured
- Preserve audit history
- Support efficient reporting
- Remain extensible

---

# 13. Summary

The database is designed around HCP interactions as the central entity. Supporting tables capture products, discussion topics, materials, samples, follow-ups, and AI conversations, allowing the CRM to provide a complete view of every HCP engagement while remaining scalable for future enterprise features.