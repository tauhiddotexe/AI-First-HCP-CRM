# AI-First CRM - HCP Interaction Logger

## Project Overview
Enterprise CRM module for pharmaceutical sales representatives. AI-first approach: users describe HCP meetings via natural language chat; LangGraph orchestrates Groq LLM (gemma2-9b-it) to extract structured data and auto-populate a split-screen enterprise form.

## Architecture Summary
- **Frontend**: React 19 + TypeScript + Redux Toolkit + TailwindCSS + React Hook Form + Axios + Lucide React
- **Backend**: Python 3.12+ + FastAPI + SQLAlchemy + Alembic + Pydantic v2
- **AI**: LangGraph + LangChain + Groq API + gemma2-9b-it (fallback: llama-3.3-70b-versatile)
- **Infrastructure**: Docker Compose (React + FastAPI + PostgreSQL)
- **Layout**: Split screen: 65% form (left), 35% AI assistant (right), full viewport, independent scrolling
- **State**: Redux Toolkit (7 slices: auth, chat, interaction, hcp, agent, ui, notification)
- **Auth**: Hardcoded demo sales rep user (server-side), designed for future JWT
- **Form Strategy**: Redux as single source of truth, React Hook Form syncs via reset()

## Key Decisions
- Full Docker Compose for all 3 services (React, FastAPI, PostgreSQL)
- No streaming (request/response chat)
- Hardcoded demo user (auto-login, no auth screen)
- Redux owns interaction state; RHF syncs bidirectionally
- CORS restricted to localhost:5173 (dev)
- Inter font via Google Fonts import
- Enterprise SaaS light theme with blue accent (#3b82f6)
- Lucide React for icons
- React Hot Toast for notifications
- Agent-browser not available (PowerShell restrictions) - used doc descriptions
- Design inspired by enterprise healthcare CRM (IQVIA, Veeva style)
- **`String(36)` over native `UUID` for primary keys** — see UUID Evaluation below

## UUID Evaluation (2026-07-08)

### Decision: Keep `String(36)`. Do NOT restore native PostgreSQL UUID.

### Analysis
Restoring native PostgreSQL `UUID` columns would require changing `BaseModel.id` and all FK columns across **11 model files** + the test repository model. The critical blocker is the `demo-rep-001` user ID stored in `User.id` and referenced as a FK in `Interaction.user_id`. This is not a valid UUID and cannot be stored in a native UUID column.

### The Mixed-Type Problem
Three options exist, all problematic:
1. **Change all IDs to UUID** — breaks `demo-rep-001` user ID pattern
2. **Change entity IDs to UUID, keep `User.id` + `Interaction.user_id` as String** — creates type inconsistency (some FKs are UUID, some are String)
3. **Keep the demo user, change all entity IDs to UUID** — requires changing `demo-rep-001` references in `config.py`, `tool_execution.py` default, `dependencies.py`, and seed data

Option 3 is the most correct but requires touching ~15 files across models, repositories, schemas, tools, seed, config, and tests. Each change is small but the aggregate risk of regression in the LangGraph workflow is non-trivial.

### Functional Impact
- `String(36)` stores UUID-format strings efficiently — PostgreSQL indexes string columns as well as UUID columns for this use case
- No functional difference in query performance at this scale
- The existing implementation is well-tested (46 passing tests)
- Frontend sends/receives IDs as strings regardless of the DB type (Pydantic serializes UUID → string)

### Bottom Line
The `String(36)` approach is consistent, working, and tested. Restoring native UUIDs would introduce unnecessary risk and complexity with no material benefit for this project. Decision: **maintain status quo.**

## Completed Tasks
### Phase 1 - Project Initialization
- Monorepo structure, Vite+React+TS frontend, FastAPI backend
- Docker Compose (3 services), all configs, env files, README
- 7 Redux slices, 10 SQLAlchemy models, Pydantic schemas
- Shared UI components, core backend config, routes, layouts
- Frontend build verified (TypeScript + Vite, 0 errors)

### Phase 2 - Backend Foundation
- Repository pattern (BaseRepository, HCPRepository, InteractionRepository)
- Service layer (HCPService, InteractionService)
- CRUD API endpoints: HCPs, Interactions, Follow-ups, Dashboard stats, Chat history
- All routers registered in FastAPI app

### Phase 3 - Frontend Foundation (UI)
- Full Interaction Form with 5 sections (Details, Discussion, Materials, Assessment, Planning)
- Each section has proper RHF integration with field arrays for dynamic arrays
- Chat Panel with polished UI (MessageBubble, ChatInput, suggested prompts)
- AI Assistant header with gradient icon, loading indicator during processing
- Empty state for chat panel ("How can I help you?")

### Phase 4 - Database Integration
- Seed script (demo user + 5 sample HCPs)
- Alembic migration setup

### Phase 5 - LangGraph Foundation
- Groq client (gemma2-9b-it + fallback llama-3.3-70b-versatile)
- Graph state definition
- All graph nodes: IntentDetection, EntityExtraction, ToolRouter, ResponseGenerator
- Graph compiled with conditional edges
- System prompt + extraction prompt templates

### Phase 6 - AI Tool Implementation
- Log Interaction tool (HCP matching, entity extraction, DB persistence)
- Edit Interaction tool (partial field update, preserve unchanged)
- Retrieve History tool (HCP lookup, chronological summary)
- Suggest Next Best Action tool (context-aware recommendations)
- Generate Visit Summary tool (manager-friendly notes)
- POST /agent/chat endpoint (end-to-end LangGraph invocation)

### Phase 7-8 - Interaction Form & Chat Interface
- See Phase 3 details above

### Phase 9 - Docker Environment Setup
- Root `docker-compose.yml` with 3 services (postgres, backend, frontend)
- `frontend/Dockerfile` — Node 20-alpine, Vite dev server with HMR + polling
- `backend/Dockerfile` — Python 3.12-slim, pip install .[dev], uvicorn --reload
- `backend/startup.sh` — Runs alembic migrations, seed data, then uvicorn
- Named volume `crm_postgres_data` for PostgreSQL persistence
- Isolated bridge network `crm-network` for inter-container communication
- Health checks for PostgreSQL (`pg_isready`) and backend (`curl /api/v1/health`)
- Service dependency: backend waits for postgres (healthy) before starting
- Bind mounts: `./backend:/app` and `./frontend:/app` for hot reload
- Vite proxy configured via `VITE_BACKEND_URL` env var (Docker service name)
- Alembic `env.py` reads `DATABASE_URL` from environment for container networking
- `.env.example` with all required variables and Docker/localhost variants
- `asyncpg` added to dependencies for PostgreSQL async support
- `aiosqlite` added to dev dependencies for test compatibility

### Phase 10 - LangGraph Bugfixes & End-to-End Verification
- **Graph routing bug**: `retrieve_history`/`suggest_action`/`generate_summary` intents bypassed `tool_router`, leaving `selected_tool` empty. Fixed in `graph.py:9` by routing all CRM intents through entity extraction.
- **EditInteraction without ID**: Tool required explicit `interaction_id` which users don't provide. Added fallback: looks up most recent interaction for matched HCP (`edit_interaction.py:20`).
- **Intent detection misclassification**: Groq model frequently returned `general` for specific CRM intents. Improved prompt with examples; default changed from `log_interaction` to `general` for safety (`intent_detection.py:14`).
- **Entity extraction too narrow**: Prompt only designed for `log_interaction` fields. Made intent-aware with dynamic instructions and guaranteed `hcp_name` extraction (`entity_extraction.py:15`).
- **Null iteration crash**: `for x in entities.get('discussion_topics', [])` crashed when entity extraction returned JSON `null` for array fields. Fixed all array iterations with `or []` pattern (`log_interaction.py:45`).
- **Input validation returning 500**: Empty/invalid input raised unhandled `ValueError`. Fixed with Pydantic `min_length`/`max_length` and `HTTPException(422)` for bad UUIDs (`agent.py:36`).
- **Suggest/Summary tools had no DB access**: Tools received empty `history`/`interaction` params. Added `_fetch_hcp_interactions()` helper that resolves HCP name and queries real DB data (`tool_execution.py:15`).
- **Shared HCP lookup logic**: Extracted `HCPRepository.find_by_name()` to eliminate duplicated HCP matching across `log_interaction.py`, `retrieve_history.py`, and `edit_interaction.py`.

## Files Created/Modified
### Docker Infrastructure
- `docker-compose.yml` (root) — 3-service compose with health checks, network, volumes
- `frontend/Dockerfile` — Multi-stage dev Dockerfile for Vite
- `frontend/.dockerignore` — Ignore node_modules, dist, logs
- `backend/Dockerfile` — Dev Dockerfile with curl, gcc, libpq-dev
- `backend/.dockerignore` — Ignore pycache, env, db files
- `backend/startup.sh` — Migration + seed + server startup script

### Config Changes
- `frontend/vite.config.ts` — Added `host: true`, `usePolling`, proxy target from env
- `backend/alembic/env.py` — Added `override_url_from_env()` for Docker networking
- `backend/app/database/engine.py` — Fixed `connect_args` NoneType bug
- `backend/app/models/base.py` — Changed `Uuid()` → `String(36)` for string ID support
- `backend/app/models/interaction.py` — FK columns `Uuid()` → `String(36)`
- `backend/app/models/discussion_topic.py` — FK column `Uuid()` → `String(36)`
- `backend/app/models/product_discussed.py` — FK column `Uuid()` → `String(36)`
- `backend/app/models/material_shared.py` — FK column `Uuid()` → `String(36)`
- `backend/app/models/sample_distributed.py` — FK column `Uuid()` → `String(36)`
- `backend/app/models/follow_up.py` — FK column `Uuid()` → `String(36)`
- `backend/app/models/chat_message.py` — FK column `Uuid()` → `String(36)`
- `backend/app/models/ai_extraction_log.py` — FK column `Uuid()` → `String(36)`
- `backend/app/core/config.py` — Added `127.0.0.1` to CORS origins
- `backend/pyproject.toml` — Added `asyncpg` and `aiosqlite` deps
- `backend/seeds/seed.py` — Made idempotent (checks for existing data)
- `.env.example` — Comprehensive with all vars, Docker/localhost variants
- `.env` — Updated for Docker networking
- `README.md` — Updated docker-compose path

### LangGraph Bugfixes
- `backend/app/graph/graph.py` — Route all CRM intents through entity_extraction (not just log/edit)
- `backend/app/graph/nodes/intent_detection.py` — Improved prompt with examples, changed default to `general`
- `backend/app/graph/nodes/entity_extraction.py` — Intent-aware extraction prompt, guaranteed `hcp_name`
- `backend/app/graph/nodes/tool_execution.py` — Added `_fetch_hcp_interactions()`, safe error handling
- `backend/app/tools/edit_interaction.py` — Added HCP-based fallback when no interaction_id provided
- `backend/app/tools/log_interaction.py` — Migrated to `HCPRepository.find_by_name()`, null-safe array iteration
- `backend/app/tools/retrieve_history.py` — Migrated to `HCPRepository.find_by_name()`
- `backend/app/repositories/hcp.py` — Added `find_by_name()` shared method
- `backend/app/api/v1/agent.py` — Pydantic input validation, proper HTTP error codes, `interaction_id` from tool result

### Cleanup
- Removed old `docker/frontend.Dockerfile`, `docker/backend.Dockerfile`, `docker/docker-compose.yml`
- Preserved `docker/postgres/init.sql`

## Issues Encountered
- PowerShell execution policy Restricted — used cmd.exe for npm commands
- Agent-browser could not be installed
- Model cannot view images directly
- TypeScript build fix: vite-env.d.ts for CSS/env types
- TypeScript unused import fixes in form components
- **Editable pip install broken by bind mount** — Changed from `pip install -e .` to `pip install .` + `PYTHONPATH=/app` so bind-mounted source takes precedence
- **UUID type incompatible with string IDs** — PostgreSQL `Uuid` column rejects `demo-rep-001`. Changed all `Uuid()` → `String(36)` in models
- **PostgreSQL FK type mismatch** — FK columns used `Uuid()` while PK columns became `String`. Changed all FK columns to `String(36)`
- **`connect_args or None` NoneType error** — `{} or None` evaluates to `None`, which isn't iterable. Refactored engine.py with conditional branches
- **Alembic hardcoded localhost URL** — Added `override_url_from_env()` in `env.py` to read `DATABASE_URL` from environment
- **Graph routing skipped non-log intents** — `should_extract()` only routed `log_interaction`/`edit_interaction` to tool execution. Fixed: route all CRM intents
- **EditInteraction required explicit UUID** — Tool returned "interaction not found" when no `interaction_id` provided. Fixed: fall back to most recent HCP interaction
- **Groq misclassified intents** — Model returned `general` for specific CRM requests. Fixed: improved prompt, added examples
- **Entity extraction missed hcp_name** — Prompt only designed for `log_interaction` fields. Fixed: intent-aware dynamic prompt
- **Null-safe array iteration** — `entities.get('discussion_topics', [])` returned `None` from JSON null. Fixed: `(entities.get('x') or [])` everywhere
- **Empty input returned 500** — Unhandled `ValueError` in validation. Fixed: Pydantic constraints + `HTTPException`
- **Suggest/Summary tools had empty data** — `NextBestAction`/`VisitSummary` received empty `history` because entity extraction doesn't produce it. Fixed: `_fetch_hcp_interactions()` queries DB directly

## Fresh Docker Verification (2026-07-08)
Performed clean-room rebuild from scratch:
1. `docker compose down -v` — full teardown, volumes deleted
2. `docker compose up --build` — all 3 images rebuilt
3. All containers healthy: postgres (16-alpine), backend, frontend (Vite 8.1.3)
4. Alembic migrations executed successfully
5. Seed data loaded: 1 user (demo-rep-001), 5 HCPs (Patel, Shah, Gupta, Verma, Reddy)
6. API endpoints verified: GET `/api/v1/health`, GET `/api/v1/hcps` (5 HCPs)
7. All 5 LangGraph tools tested end-to-end: LogInteraction, RetrieveHistory, EditInteraction, NextBestAction, VisitSummary
8. All data persisted in PostgreSQL verified via GET `/api/v1/interactions`
9. Backend tests: 20/20 passed
10. Frontend tests: 26/26 passed

## Test Results
| Suite | Tests | Status |
|-------|-------|--------|
| Backend (pytest) | 20 | ✅ All passed |
| Frontend (vitest) | 26 | ✅ All passed |
| Docker build | — | ✅ Clean build |
| LangGraph E2E | 5 tools | ✅ All verified |

## Final Project Status
- **All 5 LangGraph tools implemented and verified**: LogInteraction, EditInteraction, RetrieveHistory, NextBestAction, VisitSummary
- **LangGraph graph correctly routes all intents** through entity_extraction → tool_router → agent.py dispatch
- **Shared HCP lookup** via `HCPRepository.find_by_name()` across all tools
- **Input validation** returns proper 422 status codes for empty/too-long/invalid messages
- **Frontend**: 26 tests passing, Vite 8.1.3, React 19, Redux Toolkit
- **Backend**: 20 tests passing, FastAPI, SQLAlchemy async, Pydantic v2
- **Docker**: Full Compose setup with hot reload, health checks, seed idempotency
- **46 total tests**: all passing, all LangGraph tools working

## GitHub Repository
- **URL**: https://github.com/tauhiddotexe/AI-First-HCP-CRM.git
- **Commit**: `e380fb2` (root commit, 166 files, 19,241 insertions)
- **Branch**: `main` (also `master` as GitHub default)
- **Pushed**: 2026-07-08
- **Contents**: Full source code, Docker config, docs, tests, MEMORY.md

## Final LangGraph End-to-End Verification (2026-07-08)

### Test 1: LogInteraction ✅
| Field | Value |
|-------|-------|
| User Prompt | "I had a virtual meeting today with Dr. Priya Gupta from Children's Hospital in Bangalore. We discussed our pediatric vaccine portfolio - specifically VaxKid and ImmunoBaby..." |
| Detected Intent | `log_interaction` |
| Selected Tool | `LogInteraction` |
| Interaction ID | `de38ed12-2a66-4cb0-9115-6b9274bfebbb` |
| Form Fields | hcp_name=Dr. Priya Gupta, interaction_type=Virtual, products_discussed=[VaxKid, ImmunoBaby], sentiment=Neutral, summary=populated |
| DB Persistence | ✅ Stored in PostgreSQL with correct values |

### Test 2: RetrieveHistory ✅
| Field | Value |
|-------|-------|
| User Prompt | "Show me all my previous meetings with Dr. Priya Gupta" |
| Detected Intent | `retrieve_history` |
| Selected Tool | `RetrieveHistory` |
| Response | Accurately describes the single virtual meeting on July 8 discussing pediatric vaccine portfolio |
| DB Source | ✅ Queried from PostgreSQL (not hardcoded) |

### Test 3: EditInteraction ✅
| Field | Value |
|-------|-------|
| User Prompt | "Change the outcome of my last meeting with Dr. Gupta to Committed to Prescribe" |
| Detected Intent | `edit_interaction` |
| Selected Tool | `EditInteraction` |
| Edited ID | `de38ed12-2a66-4cb0-9115-6b9274bfebbb` |
| DB Verification | ✅ Outcome changed from "Requested More Info" to "Committed to Prescribe"; other fields unchanged |
| No ID Required | ✅ Tool found most recent interaction via HCP name matching |

### Test 4: NextBestAction ✅
| Field | Value |
|-------|-------|
| User Prompt | "What should I do next for Dr. Priya Gupta?" |
| Detected Intent | `suggest_action` |
| Selected Tool | `NextBestAction` |
| Response | Recommendations based on actual history (efficacy data, follow-up visit, samples) |
| DB Source | ✅ Queried real interactions from PostgreSQL |

### Test 5: VisitSummary ✅
| Field | Value |
|-------|-------|
| User Prompt | "Summarize my last visit with Dr. Priya Gupta" |
| Detected Intent | `generate_summary` |
| Selected Tool | `VisitSummary` |
| Response | "Your visit with Dr. Priya Gupta on 2026-07-08 has been successfully logged..." |
| DB Source | ✅ Includes HCP name, date, type, sentiment from actual DB record |

### Bugs Found & Fixed During Verification
1. **Entity extraction f-string crash**: `{` and `}` in prompt examples caused Python `ValueError: Invalid format specifier`. Fixed by escaping as `{{`/`}}`.
2. **Null product_name in samples_distributed**: LLM returned `"product_name": null` causing `NotNullViolationError`. Fixed by checking `product_name` truthiness before creating record.
3. **`find_by_name` empty last_name bug**: Single-word input like "Shah" set `last_name=""`, making `"" in hcp.last_name` always `True`, matching wrong HCPs. Fixed with prioritized matching: exact match first, last-name-only match for single words.
4. **VisitSummary "unknown HCP"**: `_fetch_hcp_interactions` didn't include HCP name in interaction dict. Fixed by adding `hcp` field.

### Final Test Results
| Suite | Tests | Status |
|-------|-------|--------|
| Backend (pytest) | 20 | ✅ All passed |
| Frontend (vitest) | 26 | ✅ All passed |
| LangGraph LogInteraction | 1 | ✅ |
| LangGraph RetrieveHistory | 1 | ✅ |
| LangGraph EditInteraction | 1 | ✅ |
| LangGraph NextBestAction | 1 | ✅ |
| LangGraph VisitSummary | 1 | ✅ |
| Intent Detection Regression | 5 inputs | ✅ All routed LogInteraction |
| DB Persistence | 4 interactions | ✅ |

## Phase 11 - Bugfixes: Intent Detection, HCP Resolution, Edit Response, Visit Ordering (2026-07-08)

### Bug 1: Intent Detection classified CRM messages as `general`
**Root cause**: Three compounding weaknesses in the intent detection pipeline:
1. **Weak prompt**: The prompt just listed examples without explicit MUST rules. The weaker fallback model (`llama-3.1-8b-instant`) frequently returned `general` for obvious `log_interaction` requests.
2. **No output normalization**: Only `.strip().lower()` was applied. Variations like "log interaction", "LogInteraction", "LOG_INTERACTION" all fell through to `general`.
3. **No deterministic fallback**: When the LLM returned an invalid label, the code blindly fell back to `general` instead of checking the message for CRM keywords.

**Files modified**:
- `backend/app/graph/nodes/intent_detection.py` — Rewrote prompt with priority-ordered rules, added `_normalize_intent()`, added `_intent_from_keywords()` deterministic fallback

**Verification**: All regression inputs → correct intent. Logs show `normalized=log_interaction`.

### Bug 2: `date.fromisoformat('yesterday')` crash
**Root cause**: Fallback LLM extracted relative dates. `date.fromisoformat()` raises `ValueError` for non-ISO strings.

**Files modified**:
- `backend/app/tools/log_interaction.py:38-46` — try/except on `fromisoformat`
- `backend/app/tools/log_interaction.py:94-97` — Same for follow_up_date
- `backend/app/tools/edit_interaction.py:40-45` — Same for edit date

### Bug 3: `Object of type date is not JSON serializable`
**Root cause**: `interaction_date` changed from string to `date` object but return dict included raw object.

**Files modified**:
- `backend/app/tools/log_interaction.py:111` — `interaction_date` → `interaction_date.isoformat()`

### Bug 4: Incorrect HCP Resolution — `find_by_name` silently substituted HCPs (Highest Priority)
**Root cause**: When both first and last name were provided (e.g., "Rajesh Gupta") and no exact match existed, `find_by_name` fell through to surname-only matching (`"gupta" == hcp.last_name.lower()`), returning the first surname match found (Priya Gupta) instead of returning "HCP not found". This affected all 5 LangGraph tools that use HCP resolution.

**Files modified**:
- `backend/app/repositories/hcp.py` — Removed surname-only fallthrough when both names are provided. If both names are given and no exact match, return `None` immediately. Single-name inputs (e.g., "Dr. Gupta") still match by surname.

**Verification**: "Dr. Rajesh Gupta" → `None` (HCP not found). "Dr. Priya Gupta" → Priya Gupta. "Dr. Sarah Patel" → Sarah Patel.

### Bug 5: EditInteraction Response Missing HCP Name
**Root cause**: `execute_edit_interaction` return dict had no `hcp_name` field. The `response_generator` node received `{'interaction_id': ..., 'updated_fields': [...], 'status': 'updated'}` — no HCP name to include in the LLM prompt.

**Files modified**:
- `backend/app/tools/edit_interaction.py:58-64` — Added HCP name resolution from interaction's HCP relationship, included `hcp_name` in return dict

**Verification**: EditInteraction response contains actual HCP name (e.g., "Dr. Rajesh Shah"), not placeholder.

### Bug 6: VisitSummary / RetrieveHistory Non-deterministic Ordering
**Root cause**: `_fetch_hcp_interactions` and `retrieve_history.py` ordered only by `interaction_date DESC`. Multiple interactions on the same date had undefined secondary ordering, causing the wrong interaction to be selected for summarization.

**Files modified**:
- `backend/app/graph/nodes/tool_execution.py:25` — Added `desc(Interaction.created_at)` as secondary sort
- `backend/app/tools/retrieve_history.py:26` — Same secondary sort

**Verification**: VisitSummary selects the most recently created interaction among same-date records.

## 5-Step Verification Conversation (All Passed)
| Step | Intent | Tool | HCP Resolved | DB Persisted |
|------|--------|------|-------------|-------------|
| 1. Log interaction with Dr. Rajesh Shah | `log_interaction` | LogInteraction | Dr. Rajesh Shah | ✅ (ID created) |
| 2. Show history for Dr. Rajesh Shah | `retrieve_history` | RetrieveHistory | Dr. Rajesh Shah | N/A |
| 3. Update latest interaction | `edit_interaction` | EditInteraction | Dr. Rajesh Shah (in response) | ✅ |
| 4. Next best action | `suggest_action` | NextBestAction | Dr. Rajesh Shah | N/A |
| 5. Generate visit summary | `generate_summary` | VisitSummary | Dr. Rajesh Shah | ✅ correct interaction |

## Ready for Submission
- ✅ Clean rebuild from scratch verified
- ✅ All 3 containers build and start correctly
- ✅ Migrations and seed data load correctly
- ✅ All 5 LangGraph tools functional end-to-end
- ✅ All data persists in PostgreSQL
- ✅ Backend test suite: 20/20
- ✅ Frontend test suite: 26/26
- ✅ UUID vs String(36) decision documented and evaluated
- ✅ Edge case handling (empty input, bad UUID, errors)
- ✅ GitHub repository pushed: https://github.com/tauhiddotexe/AI-First-HCP-CRM.git
- ✅ Commit `e380fb2` on `main` branch
- ✅ All 5 LangGraph tools verified through actual graph execution
- ✅ No backend exceptions, no frontend errors, no LangGraph node failures
- ✅ No database persistence issues
