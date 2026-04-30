# Agent Rocky — Antigravity Project Memory

## Project Goal
A personal, mobile-first AI companion focused on life management, planning, and secure personalization. Rocky lives on the user's phone, learns from uploaded files via RAG, and acts as a loyal digital ally. Security and zero-cost operation are top priorities.

## Current Phase
PHASE 1 — SETUP

## Stack
- **Backend:** Python FastAPI (Best for AI, 100% free)
- **Database / Memory:** ChromaDB (Local vector database, 100% free, highly secure)
- **Frontend:** React + Vite PWA (Mobile-first, installable on phone, 100% free)
- **Intelligence:** Google Gemini API (Free tier available)
- **Hosting Strategy:** Backend hosted on **Render** or **Hugging Face Spaces** (Free tier, zero laptop resource usage). Frontend hosted on **Vercel** (Free tier). We will ensure API keys are stored securely as Environment Secrets in the cloud.

## Agent Roster
| Agent | Specialty | Status |
|-------|-----------|--------|
| Codex | Backend / logic | IDLE |
| Gemini CLI | Feature implementation / general | IDLE |
| Copilot CLI | Tests / completions / glue code | IDLE |

## Routing Rules (Antigravity decides per task)
- **Codex** → data models, APIs, business logic, database work (Python/FastAPI)
- **Gemini CLI** → feature implementation, integrations, general coding tasks (React/Vite)
- **Copilot CLI** → unit tests, boilerplate, completions, wiring things together

## Phase Tracker
- [x] Phase 1: All context files written
- [ ] Phase 2: Coding agents activated and executing
- [ ] Phase 3: All agents report COMPLETE
- [ ] Phase 4: Debate Room review — PASS
- [ ] Phase 5: Tests pass, deployed to production

## Known Constraints
- EVERYTHING MUST BE FREE.
- Highly secure: No personal data on public servers, DB runs locally.
- Not a coding assistant: Rocky is a life planner/companion.

## Blocker Log
[Empty]
