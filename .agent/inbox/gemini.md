# Gemini CLI Inbox

## Active Task
**TASK ID:** T007
**PRIORITY:** HIGH — Send conversation history from frontend
**DESCRIPTION:**

The backend is being updated (T006) to accept a `history` field in the chat request. Update the frontend to send it.

### What To Build

#### 1. Update `frontend/src/components/ChatInterface.tsx`
- When sending a message via `axios.post`, include the full conversation history:
  ```typescript
  const history = messages.map(msg => ({
    role: msg.sender === 'user' ? 'user' : 'assistant',
    content: msg.text
  }));
  
  const response = await axios.post(`${API_URL}/api/chat`, {
    message: userMessage.text,
    history: history
  });
  ```
- This sends all previous messages so Rocky can follow the conversation

#### 2. Add markdown rendering for Rocky's replies
- Install `react-markdown`: `npm install react-markdown`
- Import it in ChatInterface.tsx
- Replace the plain `{msg.text}` in the bot message bubble with:
  ```tsx
  {msg.sender === 'bot' ? (
    <ReactMarkdown>{msg.text}</ReactMarkdown>
  ) : (
    msg.text
  )}
  ```
- Add CSS styles for rendered markdown inside `.bot .message-bubble` (headers, lists, code blocks, bold, etc.)

### Files To Change
- `frontend/src/components/ChatInterface.tsx`
- `frontend/src/components/ChatInterface.css`

### Success Criteria
1. Rocky receives full conversation history and can follow multi-turn chats
2. Rocky's responses render markdown properly (bold, lists, code blocks)

**WHEN DONE:** Update `.agent/status/gemini-status.md` and commit with message "Add conversation history + markdown rendering"
