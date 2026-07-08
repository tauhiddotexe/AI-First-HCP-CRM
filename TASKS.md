# Implementation Tasks

## Phase 1 — Project Initialization (Dependency: None)
- [x] 1.1 Create monorepo folder structure (frontend/, backend/, docs/, docker/)
- [x] 1.2 Initialize React + Vite + TypeScript frontend
- [x] 1.3 Initialize Python FastAPI backend with pyproject.toml
- [x] 1.4 Create Docker Compose (React, FastAPI, PostgreSQL) — **REWORKED**: root docker-compose.yml with health checks, networks, named volumes
- [x] 1.5 Create Dockerfiles (frontend + backend) — **REWORKED**: placed in service directories, fixed bind mount + editable install conflict
- [x] 1.6 Configure .env.example and .env — **REWORKED**: comprehensive vars for Docker networking
- [x] 1.7 Configure ESLint + Prettier (frontend)
- [x] 1.8 Configure Ruff (backend)
- [x] 1.9 Verify both apps start and Docker Compose builds — **VERIFIED**: all 3 containers healthy, APIs responding, seed data loaded
- [x] 1.10 Create README.md

## Phase 2 — Backend Foundation (Depends on: 1.3, 1.4)
- [ ] 2.1 FastAPI app factory + lifespan events
- [ ] 2.2 Application settings via pydantic-settings
- [ ] 2.3 SQLAlchemy async engine + session factory
- [ ] 2.4 Alembic configuration + initial migration
- [ ] 2.5 Base SQLAlchemy model (UUID PK, timestamps)
- [ ] 2.6 Health check endpoint (GET /api/v1/health)
- [ ] 2.7 CORS middleware (origin: localhost:5173)
- [ ] 2.8 Security headers middleware
- [ ] 2.9 Global exception handlers (400, 404, 422, 500)
- [ ] 2.10 Standard API response schemas (success/error)
- [ ] 2.11 Audit logging utility

## Phase 3 — Frontend Foundation (Depends on: 1.1, 1.2)
- [ ] 3.1 Redux store configuration + typed hooks
- [ ] 3.2 All 7 Redux slices (auth, chat, interaction, hcp, agent, ui, notification)
- [ ] 3.3 React Router setup (/, /interactions/new, /interactions/:id, /hcps, /settings)
- [ ] 3.4 TailwindCSS config + Inter font integration
- [ ] 3.5 Axios client with interceptors + base URL
- [ ] 3.6 MainLayout component (split-panel container)
- [ ] 3.7 Shared UI components (Button, Input, Select, Textarea, Badge, Card, Spinner, Modal, Avatar)
- [ ] 3.8 Auth slice with demo user auto-login
- [ ] 3.9 Notification slice + react-hot-toast integration

## Phase 4 — Database Integration (Depends on: 2.2, 2.3, 2.4, 2.5)
- [x] 4.1 SQLAlchemy models: User, HCP, Interaction, DiscussionTopic, ProductDiscussed, MaterialShared, SampleDistributed, FollowUp, ChatMessage, AIExtractionLog
- [x] 4.2 Model relationships + foreign keys + indexes
- [x] 4.3 Soft delete mixin (deleted_at)
- [ ] 4.4 Alembic migration for all tables (schema currently created via seed's create_all)
- [x] 4.5 Repository pattern (base + per entity)
- [x] 4.6 Seed script: demo user + 5 sample HCPs
- [ ] 4.7 Service layer: HCPService, InteractionService, ChatService
- [x] 4.8 CRUD API: HCP endpoints (GET list, GET by id, POST, PATCH) — **VERIFIED** via Docker
- [ ] 4.9 CRUD API: Interaction endpoints (POST, GET list w/ pagination/filter, GET by id, PATCH, DELETE soft)
- [ ] 4.10 CRUD API: FollowUp endpoints (GET list, POST, PATCH)
- [ ] 4.11 Dashboard stats endpoint (GET /dashboard)
- [ ] 4.12 Chat message endpoints (GET /chat/{interaction_id})

## Phase 5 — LangGraph Foundation (Depends on: 2.1, 2.2)
- [ ] 5.1 Groq client wrapper (langchain-groq)
- [ ] 5.2 Graph state TypedDict
- [ ] 5.3 System + developer prompt templates
- [ ] 5.4 Start node (initialize state)
- [ ] 5.5 Intent Detection node
- [ ] 5.6 Planner node
- [ ] 5.7 Tool Router node
- [ ] 5.8 Validation node
- [ ] 5.9 Response Generator node
- [ ] 5.10 Full graph compilation + conditional edges
- [ ] 5.11 State persistence / conversation memory

## Phase 6 — AI Tool Implementation (Depends on: 5.10)
- [ ] 6.1 Log Interaction tool
- [ ] 6.2 Edit Interaction tool
- [ ] 6.3 Retrieve Interaction History tool
- [ ] 6.4 Suggest Next Best Action tool
- [ ] 6.5 Generate Visit Summary tool
- [ ] 6.6 POST /agent/chat endpoint

## Phase 7 — Interaction Form (Depends on: 3.2, 3.6, 3.7, 4.9)
- [ ] 7.1 Form section components (SectionHeader, FormSection)
- [ ] 7.2 InteractionDetailsSection
- [ ] 7.3 ParticipantsSection
- [ ] 7.4 DiscussionSection
- [ ] 7.5 MaterialsSection
- [ ] 7.6 AssessmentSection
- [ ] 7.7 PlanningSection
- [ ] 7.8 NotesSection
- [ ] 7.9 Form validation
- [ ] 7.10 AI-updated field visual indicator
- [ ] 7.11 React Hook Form -> Redux sync hook
- [ ] 7.12 Loading/error states

## Phase 8 — AI Chat Interface (Depends on: 3.2, 3.6, 3.7, 6.6)
- [ ] 8.1 ChatPanel container
- [ ] 8.2 ChatHistory component
- [ ] 8.3 MessageBubble component
- [ ] 8.4 ChatInput component
- [ ] 8.5 LoadingIndicator component
- [ ] 8.6 SuggestedPrompts component
- [ ] 8.7 Dispatch chat thunk
- [ ] 8.8 Handle response

## Phase 9 — End-to-End Integration (Depends on: 7.12, 8.8)
- [ ] 9.1 Full flow: chat -> LangGraph -> tool -> DB -> Redux -> form update
- [ ] 9.2 Edit flow
- [ ] 9.3 History retrieval
- [ ] 9.4 Next best action suggestion
- [ ] 9.5 Visit summary generation
- [ ] 9.6 Toast notifications
- [ ] 9.7 Network error handling
- [ ] 9.8 Loading states

## Phase 10 — Testing & Polish (Depends on: 9.8)
- [ ] 10.1 Backend unit tests
- [ ] 10.2 Backend API tests
- [ ] 10.3 LangGraph workflow tests
- [ ] 10.4 Frontend unit tests
- [ ] 10.5 Form validation tests
- [ ] 10.6 Chat integration test
- [ ] 10.7 Accessibility audit
- [ ] 10.8 Responsive check
- [ ] 10.9 UI polish pass
- [ ] 10.10 Performance optimization
- [ ] 10.11 Final README
- [ ] 10.12 Security checklist verification
