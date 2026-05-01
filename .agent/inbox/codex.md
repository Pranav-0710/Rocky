# Codex Inbox

## Active Task
**TASK ID:** T006
**PRIORITY:** HIGH — Add conversation history to Rocky
**DESCRIPTION:**

Right now Rocky has no short-term memory. Every message is treated independently — he can't follow a multi-turn conversation. Fix this.

### What To Build

#### 1. Add conversation history to the chat endpoint
In `backend/app/routes/chat.py`:
- Change `ChatRequest` to accept an optional `history` field: a list of `{"role": "user"|"assistant", "content": "..."}` objects
- Pass the full history to `get_reply()` instead of just the latest message

#### 2. Update `backend/app/services/llm.py`
- Change `get_reply()` signature to accept `history: list[dict]` instead of just `message: str`
- Build the messages array properly:
  - First message: `{"role": "system", "content": system_prompt}` (keep existing system prompt with context)
  - Then append all history messages
  - Final message: the current user message
- This gives Rocky full conversation awareness

#### 3. Keep backward compatibility
- If `history` is empty or not provided, behave exactly as before (single message mode)

### Files To Change
- `backend/app/routes/chat.py`
- `backend/app/services/llm.py`

### Success Criteria
Rocky should be able to follow up. Example:
- User: "My cat's name is Luna"
- Rocky: "Luna is a beautiful name!"
- User: "What's her name again?"
- Rocky: "Your cat's name is Luna!" (NOT "I don't know")

**WHEN DONE:** Update `.agent/status/codex-status.md` and commit with message "Add conversation history support"
