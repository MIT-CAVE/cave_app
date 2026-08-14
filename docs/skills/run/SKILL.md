---
name: run
description: Launch the CAVE app in Docker via `cave run`, confirm it's actually serving, and open/drive it in the browser at localhost:8000/cave/. Use when asked to run, start, launch, or verify the app is working end-to-end — not just `cave test`.
---

# Running the CAVE App

`cave run` builds and starts the app's Docker containers (Postgres, the Django ASGI server, etc.) — see [cave-cli](../cave-cli/SKILL.md) for the full command reference. This skill is specifically about getting a running instance you can look at and verify.

## 1. Start it

`cave run` is a long-running foreground process — run it in the background and watch its output rather than blocking on it:

```
cave run
```

First boot runs `manage.py check`, ensures Postgres is up, and applies DB setup/migrations — this can take noticeably longer than subsequent starts.

To run on a specific LAN `ip:port` instead of localhost (uses a self-signed SSL cert — see `utils/lan_hosting/readme.md`):
```
cave run <ip>:<port>
```

## 2. Confirm it's actually serving

Poll the base URL rather than trusting the log stream — the container can report as running before Django finishes its startup checks. There's a real loading period on first boot (waiting for Postgres, `manage.py check`, DB migrations) — give it room, but cap how long you wait:

```
timeout 30 bash -c 'until curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/cave/ | grep -q 200; do sleep 3; done'
```

If it never comes up within that window, don't keep waiting or retry silently — notify the user that startup is stuck (include whatever the logs show) and run `cave kill` to stop it rather than leaving a hung container running.

## 3. Open and drive it

The app lives at `http://localhost:8000/cave/` — Chrome is the only fully supported browser.

- Most of the app requires being logged in. The default admin's credentials are in this project's `.env` (`DJANGO_ADMIN_USERNAME` / `DJANGO_ADMIN_PASSWORD`) — treat `.env` as a secrets file: look up a specific key if you need it, don't cat/print/paste its full contents into chat or logs.
- After login, click the app-page icon, then the examples switcher (three sliders, top left) to browse the bundled `cave_api/examples/` — see the [examples](../examples/SKILL.md) skill.
- A blank/grey screen after load means a frontend error, not necessarily a Python one — see the [debug](../debug/SKILL.md) skill (start with the browser console, `Ctrl+Shift+i`).

`cave test init.py` (see [test](../test/SKILL.md)) validates your `execute_command` output headlessly and is faster for iterating on API changes. Reach for a real run when you need to see the rendered UI itself, not just validate the schema.

## 4. Stop it

`cave kill` stops the containers — it's in the destructive tier of [cave-cli](../cave-cli/SKILL.md), so confirm with the user before running it. The one exception is the stuck-startup case in step 2: there, notifying the user *is* the confirmation — kill it right after telling them, don't leave a hung container running while waiting on a reply.
