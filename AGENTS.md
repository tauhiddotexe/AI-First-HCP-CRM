# AI Agents Memory

## Project
Enterprise AI-First CRM - HCP Interaction Logger with LangGraph-powered NL interaction logging.

## Tech Stack
- **Frontend**: React 19, TypeScript 6, Redux Toolkit, TailwindCSS 3, React Hook Form, Vite 8, Lucide
- **Backend**: Python 3.12+, FastAPI, SQLAlchemy 2.0 (async), Alembic, Pydantic v2
- **AI**: LangGraph, LangChain, Groq API (gemma2-9b-it, fallback: llama-3.3-70b-versatile)
- **Infra**: Docker Compose (frontend, backend, PostgreSQL)
- **Code Quality**: oxlint (frontend), ruff + mypy strict (backend)

## Testing
- **Frontend**: `cd frontend && npm test` (vitest)
- **Backend**: `cd backend && python -m pytest` (pytest + pytest-asyncio)
- Backend tests set `DATABASE_URL=sqlite+aiosqlite:///:memory:` automatically in conftest.py

## Naming
- Routes: prefix per domain (`/interactions`, `/hcps`, `/agent/chat`)
- Schemas: `{Entity}Create`, `{Entity}Update`, `{Entity}Response`
- Services: `{Domain}Service`
- Repositories: `{Entity}Repository`
- Redux: `{domain}Slice`, e.g. `interactionSlice`

## Conventions
- No streaming (request/response chat)
- Hardcoded demo user (`demo-rep-001`)
- Redux as single source of truth; RHF initialized from Redux via reset()
- Repository pattern: BaseRepository → EntityRepository → Service → Router
- PostgreSQL in production; SQLite for tests (generic `Uuid` and `JSON` types used)
- Inter font, enterprise SaaS light theme, blue accent (#3b82f6), split-screen 65/35
- No AI slop patterns (generic names, filler verbs, 3-column equal cards — banned)

## Key Commands
- `cd frontend && npm run dev` — start frontend
- `cd backend && python -m uvicorn app.main:app --reload` — start backend
- `cd frontend && npm run build` — build frontend (tsc + vite)
- `docker compose -f docker/docker-compose.yml up` — full stack

## Architecture
- 7 Redux slices: auth, chat, interaction, hcp, agent, ui, notification
- 6 LangGraph tools: LogInteraction, EditInteraction, RetrieveHistory, NextBestAction, VisitSummary, ChatWithHuman
- 5 LangGraph intents: log_interaction, edit_interaction, retrieve_history, suggest_action, generate_summary
- Agent chat → IntentDetection → EntityExtraction → ToolRouter → ResponseGenerator
- Graph compiled with StateGraph, conditional edges per intent

## Key Files
- `frontend/src/redux/slices/chatSlice.ts` — sendMessage thunk dispatches updateFormFromAI on fulfillment
- `frontend/src/features/chat/components/ChatPanel.tsx` — watches lastResponse, dispatches form updates
- `frontend/src/features/interaction/components/HCPSelect.tsx` — searchable dropdown via Redux
- `backend/app/graph/graph.py` — compiled LangGraph with conditional routing
- `backend/app/api/v1/agent.py` — POST /agent/chat endpoint
- `backend/app/main.py` — FastAPI app with CORS, exception handlers, router registration
