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
