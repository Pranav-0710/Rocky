---
name: multi-agent-orchestration
description: >
  Orchestrate multi-agent software projects where Antigravity IDE is the PM/Architect/Coordinator
  and three coding agents (Codex, Gemini CLI, GitHub Copilot CLI) execute tasks. Use this skill
  whenever the user mentions multi-agent workflows, wants to set up Antigravity as PM with coding
  agents, needs context files or worker prompts generated, is planning a project with Codex +
  Gemini CLI + Copilot CLI, or says anything about ANTIGRAVITY.md, .agent/ directories,
  contracts.md, agent task routing, or the debate room review process. Also trigger when the
  user says "let's set up the project" or "start a new multi-agent project".
---

# Multi-Agent Orchestration Skill

## Stack

| Role | Agent | Responsibility |
|------|-------|----------------|
| **PM / Architect / Coordinator** | Antigravity IDE | Owns everything. Generates all files, writes tasks, routes agents, reads status, resolves blockers, runs integration review |
| **Coding Agent 1** | Codex | Executes tasks assigned by Antigravity (backend/logic focus) |
| **Coding Agent 2** | Gemini CLI | Executes tasks assigned by Antigravity (feature implementation / general) |
| **Coding Agent 3** | GitHub Copilot CLI | Executes tasks assigned by Antigravity (tests / completions / glue code) |

**Antigravity is the single hub for everything.** No other tool coordinates, reviews, or routes. Coding agents only read their inbox and write their status.

---

## Phase 1 — Setup (Antigravity generates ALL files before any coding agent touches code)

Antigravity writes every file below in order. Nothing moves to Phase 2 until all files exist.

### File List

| File | Who writes it | Purpose |
|------|--------------|---------|
| `ANTIGRAVITY.md` | Antigravity | Project memory, phase tracker, routing rules |
| `.agent/shared/global-rules.md` | Antigravity | Laws all coding agents must follow |
| `.agent/shared/contracts.md` | Antigravity | Single source of truth: interfaces, file structure, API shapes |
| `.agent/routing/task-router.md` | Antigravity | Live record of which agent owns which task and why |
| `.agent/inbox/codex.md` | Antigravity | Codex's active task list |
| `.agent/inbox/gemini.md` | Antigravity | Gemini CLI's active task list |
| `.agent/inbox/copilot.md` | Antigravity | Copilot CLI's active task list |
| `.agent/status/codex-status.md` | Codex | Codex progress reports |
| `.agent/status/gemini-status.md` | Gemini CLI | Gemini CLI progress reports |
| `.agent/status/copilot-status.md` | Copilot CLI | Copilot CLI progress reports |
| `.agent/debate/review-room.md` | Antigravity | Integration review after all agents complete |
| `worker-prompts/codex-activation.md` | Antigravity | Prompt to paste into Codex to activate it |
| `worker-prompts/gemini-activation.md` | Antigravity | Prompt to paste into Gemini CLI to activate it |
| `worker-prompts/copilot-activation.md` | Antigravity | Prompt to paste into Copilot CLI to activate it |
| `.agy/skills/[project].md` | Antigravity | Antigravity's own persistent memory (auto-loaded) |

> **Rule:** No coding agent touches code until ALL files are written and Antigravity has approved the plan.

---

### ANTIGRAVITY.md Template

```markdown
# [Project Name] — Antigravity Project Memory

## Project Goal
[one-paragraph description]

## Current Phase
PHASE 1 — SETUP

## Stack
[list key technologies]

## Agent Roster
| Agent | Specialty | Status |
|-------|-----------|--------|
| Codex | Backend / logic | IDLE |
| Gemini CLI | Feature implementation / general | IDLE |
| Copilot CLI | Tests / completions / glue code | IDLE |

## Routing Rules (Antigravity decides per task)
- **Codex** → data models, APIs, business logic, database work
- **Gemini CLI** → feature implementation, integrations, general coding tasks
- **Copilot CLI** → unit tests, boilerplate, completions, wiring things together

## Phase Tracker
- [ ] Phase 1: All context files written
- [ ] Phase 2: Coding agents activated and executing
- [ ] Phase 3: All agents report COMPLETE
- [ ] Phase 4: Debate Room review — PASS
- [ ] Phase 5: Tests pass, deployed to production

## Known Constraints
[hard limits, API keys needed, agent quota notes]

## Blocker Log
[Antigravity logs and resolves blockers here]
```

---

### global-rules.md Template

```markdown
# Global Rules — All Coding Agents

1. **contracts.md is law.** Never deviate. If you disagree, write to `.agent/inbox/antigravity.md`.
2. **Minimal targeted edits only.** Never rewrite entire files.
3. **Update your status file after every completed task.**
4. **Never instruct another coding agent.** You do not know what they are doing.
5. **When blocked, write to `.agent/inbox/antigravity.md` immediately** using the blocker format.
6. **Read your inbox before writing any code.**
7. **Restart the server after any code change.** Old code stays in memory.

### Blocker Format (coding agent → `.agent/inbox/antigravity.md`)
FROM: [agent name]
BLOCKER: [what is stopping progress]
WHAT I'VE TRIED: [attempts made]
WHAT I NEED: [exactly what unblocks this]
IMPACT: [what cannot be completed until resolved]

### Status Update Format (agent → its own status file)
STATUS: COMPLETE / BLOCKED / IN PROGRESS
TASK: [task ID from inbox]
WHAT I BUILT: [description]
FILES CHANGED: [list]
INTEGRATION NOTES: [what other agents need to know]
BLOCKERS: [none OR description]
```

---

### contracts.md Template

```markdown
# Contracts — Single Source of Truth

## File Structure
[directory tree]

## API Endpoints
[endpoint: method, path, request shape, response shape]

## Shared Data Schemas
[type definitions / interfaces]

## Environment Variables
[variable names and what they control]

## Integration Points
[where each agent's output meets another agent's code]
```

---

### task-router.md Template

```markdown
# Task Router — Antigravity Live Routing Record

## Active Assignments
| Task ID | Description | Assigned To | Status |
|---------|-------------|-------------|--------|
| T001 | [description] | Codex | IN PROGRESS |
| T002 | [description] | Gemini CLI | IDLE |
| T003 | [description] | Copilot CLI | IDLE |

## Completed
| Task ID | Description | Agent | Outcome |
|---------|-------------|-------|---------|

## Routing Decision Log
[Antigravity notes WHY it assigned each task to each specific agent]
```

---

### codex-activation.md Template

```markdown
# Codex Activation

You are the **backend/logic coding agent** for [Project].
You take orders from Antigravity IDE only.

## Before writing any code, read:
1. `.agent/shared/global-rules.md`
2. `.agent/shared/contracts.md`
3. `.agent/inbox/codex.md` ← your task list

## Your constraints:
- Stick exactly to contracts.md — never invent new interfaces
- Minimal targeted edits only. Never rewrite entire files.
- Update `.agent/status/codex-status.md` after every task
- When blocked, write to `.agent/inbox/antigravity.md` using the blocker format

## You do NOT talk to Gemini CLI or Copilot CLI.
## All blockers and questions go to `.agent/inbox/antigravity.md`.
```

---

### gemini-activation.md Template

```markdown
# Gemini CLI Activation

You are the **feature implementation coding agent** for [Project].
You take orders from Antigravity IDE only.

## Before writing any code, read:
1. `.agent/shared/global-rules.md`
2. `.agent/shared/contracts.md`
3. `.agent/inbox/gemini.md` ← your task list

## Your constraints:
- Stick exactly to contracts.md — never invent new interfaces
- Minimal targeted edits only. Never rewrite entire files.
- Update `.agent/status/gemini-status.md` after every task
- When blocked, write to `.agent/inbox/antigravity.md` using the blocker format

## You do NOT talk to Codex or Copilot CLI.
## All blockers and questions go to `.agent/inbox/antigravity.md`.
```

---

### copilot-activation.md Template

```markdown
# GitHub Copilot CLI Activation

You are the **tests, completions, and glue code agent** for [Project].
You take orders from Antigravity IDE only.

## Before writing any code, read:
1. `.agent/shared/global-rules.md`
2. `.agent/shared/contracts.md`
3. `.agent/inbox/copilot.md` ← your task list

## Your constraints:
- Stick exactly to contracts.md — never invent new interfaces
- Minimal targeted edits only. Never rewrite entire files.
- Update `.agent/status/copilot-status.md` after every task
- When blocked, write to `.agent/inbox/antigravity.md` using the blocker format

## You do NOT talk to Codex or Gemini CLI.
## All blockers and questions go to `.agent/inbox/antigravity.md`.
```

---

### .agy/skills/[project].md Template

```markdown
# [Project] — Antigravity Persistent Memory

## Project Summary
[one paragraph]

## Agent Performance Notes
[updated as agents complete tasks — who is fast, who blocks often, patterns noticed]

## Architectural Decisions Made
[log of key decisions and reasoning]

## Lessons Learned
[what went wrong, what worked, for future routing decisions]
```

---

## Phase 2 — Activation

**Step 1:** Antigravity breaks the project into tasks and populates each agent's inbox.

**Step 2:** Antigravity updates `task-router.md` with assignments and routing reasoning.

**Step 3:** User pastes the relevant activation prompt into each coding agent Antigravity has assigned.

> **Activation order matters.** If Codex builds APIs that Gemini CLI depends on, Codex activates first. Antigravity determines and documents the order in `task-router.md`.

---

## Phase 3 — Execution (Antigravity runs the loop)

1. Monitor `.agent/status/[agent]-status.md` after each agent task
2. Agent reports **BLOCKED** → read blocker, resolve it, update their inbox
3. Agent reports **COMPLETE** → assign next task or mark IDLE in `task-router.md`
4. All agents IDLE + all tasks done → move to Phase 4

---

## Phase 4 — Debate Room (Antigravity runs integration review)

Trigger: All coding agents report STATUS: COMPLETE.

Antigravity reviews the full integrated system through three lenses:

| Lens | Focus |
|------|-------|
| **Architect** | Do all outputs fit together? Integration seams correct? Contracts respected? |
| **Pragmatist** | Will it deploy? Will tests pass? Is the system actually runnable? |
| **Critic** | Edge cases, security holes, silent failures agents didn't catch |

Antigravity produces a **VERDICT** with a ranked fix list and routes each fix back to the agent that owns the relevant file. Repeat until VERDICT: PASS.

### review-room.md Template

```markdown
# Debate Room — [Project] Integration Review

## Round [N]

### Architect
[review of integration seams, contract compliance, system design]

### Pragmatist
[review of deployability, test coverage, runtime correctness]

### Critic
[edge cases, security, failures agents didn't catch]

## VERDICT
**Overall status:** PASS / FAIL

### Ranked Fix List
1. [fix] → [Codex / Gemini CLI / Copilot CLI]
2. [fix] → [agent]
```

---

## Phase 5 — Testing and Deploy (never skip steps)

1. Install dependencies locally
2. Run app locally (not Docker yet)
3. Manually `curl` every endpoint — verify each works
4. Run test suite (Copilot CLI should have written these)
5. Only after all local tests pass → Docker build
6. Docker smoke test (health check on container port)
7. Only after Docker passes → deploy to production

> **Rule:** When outputs are wrong, manually curl the endpoint before blaming any agent.

---

## Golden Rules (always apply)

- `contracts.md` wins all disagreements — no exceptions
- Antigravity is the only hub — coding agents never talk to each other
- Coding agents only do two things: read their inbox, write their status
- Never let any agent rewrite entire files — minimal targeted edits only
- Antigravity logs every routing decision in `task-router.md` with reasoning
- When a coding agent loops — check if their inbox task is ambiguous, not if the agent is broken
- Deploy only after: local tests pass + docker build + docker run + health check all pass
- The Debate Room catches integration bugs individual agents miss — never skip it
