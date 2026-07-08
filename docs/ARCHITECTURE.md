# System Architecture

# AI-First CRM – HCP Interaction Logger

Version: 1.0

---

# 1. Purpose

This document defines the technical architecture for the AI-First CRM application. It describes the overall system design, component interactions, request lifecycle, frontend architecture, backend architecture, LangGraph orchestration, data flow, and design principles.

The goal is to establish a scalable, maintainable, AI-first architecture suitable for enterprise healthcare CRM systems.

---

# 2. Architecture Goals

The architecture should prioritize:

- AI-first user experience
- Modular services
- Separation of concerns
- Scalability
- Maintainability
- Reusability
- Strong typing
- Easy testing
- Enterprise-grade project structure

---

# 3. Technology Stack

## Frontend

- React 19
- TypeScript
- Redux Toolkit
- React Router
- TailwindCSS
- React Hook Form
- Axios

---

## Backend

- Python 3.12+
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic v2
- PostgreSQL

---

## AI

- LangGraph
- LangChain
- Groq API
- gemma2-9b-it
- Optional fallback:
    - llama-3.3-70b-versatile

---

## Infrastructure

- Docker
- Docker Compose

---

# 4. High-Level Architecture

                    Browser
                        │
                        ▼
              React Application
                        │
          Redux Global State
                        │
                 API Service Layer
                        │
                 HTTP (REST API)
                        │
                     FastAPI
                        │
            -------------------------
            |                       |
      Business Logic         LangGraph Agent
            |                       |
            |                Tool Router
            |                       |
            |          Groq LLM + CRM Tools
            |                       |
            --------Validation-------
                        │
                 PostgreSQL Database

---

# 5. System Components

The system is divided into four major layers.

## Presentation Layer

Responsible for rendering UI.

Includes:

- Pages
- Components
- Forms
- Chat Interface
- Layout
- Navigation

No business logic should exist here.

---

## State Layer

Redux manages:

- Authentication
- Chat history
- Form state
- HCP data
- Agent responses
- Loading states
- Errors

API calls should never directly mutate components.

---

## Backend Layer

Responsible for:

- Request validation
- Authentication
- Database operations
- LangGraph execution
- Tool orchestration

Business logic remains independent from API endpoints.

---

## AI Layer

Responsible for:

- Intent recognition
- Entity extraction
- Tool routing
- Conversation reasoning
- Structured data generation
- Response generation

This layer is implemented entirely using LangGraph.

---

# 6. Frontend Architecture

Frontend follows feature-based architecture.

src/

components/

pages/

features/

redux/

hooks/

services/

types/

utils/

assets/

styles/

---

## Components

Components should remain reusable.

Examples:

- Button
- Card
- Input
- Modal
- ChatBubble
- FormField
- Sidebar

---

## Pages

Main pages include:

Dashboard

HCP List

Interaction Logger

Interaction Details

Settings

---

## Feature Modules

Each feature owns:

components

hooks

redux

services

types

Example

features/

interaction/

chat/

hcp/

dashboard/

---

# 7. Backend Architecture

Backend follows layered architecture.

app/

api/

core/

agents/

graph/

tools/

services/

repositories/

models/

schemas/

database/

prompts/

utils/

---

## API Layer

Only handles:

- validation
- serialization
- responses

No AI logic.

---

## Service Layer

Contains business logic.

Examples:

InteractionService

HCPService

ChatService

---

## Repository Layer

Handles all database operations.

No SQL should exist in services.

---

## AI Layer

Contains:

Graph

Nodes

Prompts

Tool definitions

State schema

Memory

---

# 8. LangGraph Architecture

LangGraph acts as the intelligent orchestration engine.

Responsibilities

Understand user intent.

Select appropriate tool.

Generate structured data.

Validate extraction.

Persist data.

Generate response.

---

## Graph Flow

User Message

↓

Intent Detection

↓

Planner Node

↓

Tool Selection

↓

Execute Tool

↓

LLM Processing

↓

Validation

↓

Database

↓

Generate Response

↓

Frontend Update

---

## Graph Nodes

Start

Intent Detection

Planner

Tool Router

Tool Execution

Validation

Persistence

Response Generator

End

---

## Supported Tools

Log Interaction

Edit Interaction

Retrieve Interaction History

Suggest Next Best Action

Generate Visit Summary

Additional tools should be easily pluggable.

---

# 9. Request Lifecycle

Example:

User:

"I met Dr Shah today. He liked Product X but wants more efficacy data."

↓

Frontend

↓

Redux

↓

POST /agent/chat

↓

FastAPI

↓

LangGraph

↓

Intent Detection

↓

Log Interaction Tool

↓

Groq LLM

↓

Extract

Doctor

Product

Sentiment

Follow-up

Summary

↓

Validation

↓

Save Database

↓

Return JSON

↓

Redux Update

↓

Form Automatically Updates

↓

Assistant Confirmation

---

# 10. Data Flow

Natural Language

↓

LLM Extraction

↓

Structured JSON

↓

Validation

↓

Database

↓

API Response

↓

Redux Store

↓

UI

---

# 11. Form Synchronization

The interaction form is synchronized with AI output.

Rules:

AI updates only changed fields.

Existing values remain.

Manual edits remain unless explicitly overridden.

Redux remains single source of truth.

---

# 12. State Management

Redux slices

auth

chat

interaction

hcp

agent

ui

notifications

---

State flow

User Action

↓

Dispatch

↓

API

↓

Reducer

↓

Store

↓

UI

---

# 13. Database Layer

Main entities

User

HCP

Interaction

ChatMessage

FollowUp

Material

Sample

Relationships

User

↓

Interactions

↓

HCP

One HCP may have many interactions.

One interaction belongs to one HCP.

---

# 14. Error Handling

Frontend

Display friendly messages.

Retry transient failures.

Prevent duplicate submissions.

Backend

Validation errors

Database errors

LLM failures

Network failures

Gracefully handled.

---

# 15. Security

Input validation

SQL injection protection

Environment variables

Server-side API keys

Parameterized queries

Prompt sanitization

No sensitive credentials exposed to frontend.

---

# 16. Scalability

Architecture should support:

Additional AI tools

Multiple agents

Analytics dashboard

Voice logging

Speech-to-text

Calendar integration

RAG

Workflow automation

CRM integrations

---

# 17. Design Principles

Single Responsibility Principle

Dependency Injection

Reusable Components

Feature-based Organization

Thin Controllers

Service Layer Pattern

Repository Pattern

Strong Typing

Immutable Redux State

Stateless APIs

Modular LangGraph Nodes

---

# 18. Future Architecture

The architecture should be designed so additional agents can be introduced.

Examples:

Scheduling Agent

Analytics Agent

Reporting Agent

Email Agent

Reminder Agent

Medical Information Agent

Each agent should expose tools while sharing the same database and API layer.

---

# 19. Summary

The application follows a layered enterprise architecture centered around LangGraph. React provides the presentation layer, Redux manages application state, FastAPI exposes APIs, PostgreSQL stores structured CRM data, and LangGraph orchestrates all AI reasoning and tool execution.

The architecture intentionally separates UI, business logic, AI workflows, and persistence to maximize maintainability, extensibility, and code quality.