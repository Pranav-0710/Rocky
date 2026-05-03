# Gemini CLI Inbox

## Active Task
**TASK ID:** T010
**PRIORITY:** HIGH — Rocky's avatar + UI personality upgrade
**DESCRIPTION:**

Rocky needs to LOOK like Rocky. He is the spider-like Eridian alien from *Project Hail Mary* by Andy Weir. His photo is at `c:\PROJECTS\Rocky\rocky photo.webp`.

### What To Build

#### 1. Copy Rocky's photo into the frontend public folder
The file `rocky photo.webp` is at the project root. Copy it to `frontend/public/rocky.webp` so it is accessible at `/rocky.webp` in the deployed app.

#### 2. Update `frontend/src/components/ChatInterface.tsx`
- **Bot avatar:** In the message list, show Rocky's avatar image (`/rocky.webp`) next to every bot message bubble.
  - Add an `<img src="/rocky.webp" className="rocky-avatar" alt="Rocky" />` element inside `.message-wrapper.bot` before the `.message-bubble`
- **Header:** Replace the plain "Rocky AI" text header with:
  - Rocky's avatar image (small, ~36px circle) on the left
  - "Rocky" as the name
  - Subtitle: "Eridian Engineer · Online" (green dot)
  - Remove the old separate status dot

#### 3. Update `frontend/src/components/ChatInterface.css`
Add styles for:
```css
.rocky-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  border: 1px solid rgba(255,255,255,0.15);
}

.message-wrapper.bot {
  display: flex;
  align-items: flex-end;
  gap: 8px;
}

.chat-header {
  /* Update to show avatar + name + subtitle */
  display: flex;
  align-items: center;
  gap: 12px;
}

.chat-header .header-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #4ade80;
}

.chat-header .header-info {
  display: flex;
  flex-direction: column;
}

.chat-header .header-name {
  font-weight: 700;
  font-size: 1rem;
  color: #fff;
}

.chat-header .header-subtitle {
  font-size: 0.7rem;
  color: #4ade80;
  letter-spacing: 0.05em;
}
```

#### 4. Update the auth/PIN screen in `ChatInterface.tsx`
- Replace the `<img src="/logo.png">` on the PIN screen with `<img src="/rocky.webp">`
- Change the subtitle from "Please enter your secure PIN" to:
  *"Verify identity, human."*
- Change the button text from "Unlock Ally" to:
  *"Authenticate"*

### Files To Change
- `frontend/public/rocky.webp` (copy from project root)
- `frontend/src/components/ChatInterface.tsx`
- `frontend/src/components/ChatInterface.css`

### Success Criteria
1. Rocky's stone-spider image appears as the avatar next to every bot message
2. The header shows Rocky's face + "Rocky" + "Eridian Engineer · Online"
3. The PIN screen shows Rocky's photo and says "Verify identity, human."

**WHEN DONE:** Update `.agent/status/gemini-status.md` and commit with message "Rocky avatar + UI personality upgrade"
