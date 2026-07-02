---
name: debug
description: Debug a CAVE API app that isn't behaving as expected — validation errors, blank/grey screen, or unexpected session state. Use when asked to debug, troubleshoot, or investigate why something isn't working.
---

# Debugging

| Tool | How |
|---|---|
| Print statements | Add `print(...)` in `cave_api/` — output appears in the `cave run` terminal (hot-reloads, no restart needed) |
| Manual validation | `cave test init.py` — runs `Validator` against your `init` output and prints structured logs |
| Live validation | Set `LIVE_API_VALIDATION_PRINT=true` in `.env`, then restart with `cave run` |
| Browser console | `Ctrl+Shift+i` → Console tab — a grey/blank screen after `init` usually means a frontend error here, not a Python exception |

Start with `cave test init.py` for any structural/schema problem (missing required field, wrong type, bad prop reference) — the `Validator` log points at the exact path. Reach for the browser console only once `init.py` passes but the UI still looks wrong.
