# AI-First CRM - HCP Interaction Logger

Enterprise CRM module for pharmaceutical sales representatives. An AI-first approach where users describe HCP meetings via natural language chat, and the system intelligently extracts structured data to auto-populate a split-screen interaction form.

## Architecture

```
Frontend (React 19 + TypeScript + Redux Toolkit + TailwindCSS)
    |
Backend (FastAPI + SQLAlchemy + LangGraph + Groq LLM)
    |
Database (PostgreSQL)
```

### Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, TypeScript, Redux Toolkit, TailwindCSS, React Hook Form, Axios |
| Backend | Python 3.12+, FastAPI, SQLAlchemy, Alembic, Pydantic v2 |
| AI | LangGraph, LangChain, Groq API (gemma2-9b-it) |
| Infrastructure | Docker, Docker Compose, PostgreSQL 16 |

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 20+
- Python 3.12+
- Groq API key (get one at https://console.groq.com)

### Setup

1. Clone the repository:
```bash
git clone <repo-url>
cd ai-first-crm
```

2. Copy environment variables:
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

3. Start with Docker Compose:
```bash
docker compose up --build
```

4. Access the application:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/docs

### Local Development

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Backend:**
```bash
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## Project Structure

```
ai-first-crm/
├── frontend/          # React application
│   ├── src/
│   │   ├── components/    # Shared UI components
│   │   ├── features/      # Feature modules
│   │   ├── layouts/       # Layout components
│   │   ├── pages/         # Route pages
│   │   ├── redux/         # Redux store & slices
│   │   ├── services/      # API client
│   │   ├── types/         # TypeScript types
│   │   └── utils/         # Utilities
│   └── ...
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── core/          # Config & dependencies
│   │   ├── agents/        # LangGraph agent
│   │   ├── graph/         # Graph nodes & state
│   │   ├── tools/         # CRM tools
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── repositories/  # Data access
│   │   ├── database/      # DB connection
│   │   └── prompts/       # LLM prompts
│   └── ...
├── docker/            # Postgres init scripts
└── docs/              # Project documentation
```

## LangGraph Tools

1. **Log Interaction** - Create structured CRM interaction from natural language
2. **Edit Interaction** - Modify specific fields of existing interactions
3. **Retrieve History** - Fetch and summarize previous HCP interactions
4. **Suggest Next Action** - Recommend follow-up actions based on history
5. **Generate Summary** - Produce manager-friendly visit summaries

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/health | Health check |
| POST | /api/v1/agent/chat | AI chat endpoint |
| GET/POST | /api/v1/hcps | List/Create HCPs |
| GET/PATCH | /api/v1/hcps/{id} | Get/Update HCP |
| POST | /api/v1/interactions | Create interaction |
| GET | /api/v1/interactions | List interactions |
| GET/PATCH/DELETE | /api/v1/interactions/{id} | Get/Update/Delete |
| GET | /api/v1/dashboard | Dashboard stats |
