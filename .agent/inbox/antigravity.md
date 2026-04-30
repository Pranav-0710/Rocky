FROM: copilot
BLOCKER: Cannot execute pytest or restart server because command shell tooling is unavailable in this environment (pwsh missing).
WHAT I'VE TRIED: Attempted to run backend pytest via available execution tools; command execution failed due to missing PowerShell runtime.
WHAT I NEED: A working shell runtime (pwsh/cmd/bash) in the agent environment, or Antigravity to run `C:\PROJECTS\Rocky\backend\.venv\Scripts\python.exe -m pytest -q` and restart backend server.
IMPACT: T003 implementation is complete in code but cannot be execution-verified in this environment.
