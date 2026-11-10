---
name: run
description: Launch the CAVE app in Docker via `cave run`, confirm it's actually serving, and open/drive it in the browser at localhost:8000/cave/. Use when asked to run, start, launch, or verify the app is working end-to-end — not just `cave test`.
---

# Running the CAVE App

`cave run` builds and starts the app's Docker containers (Postgres, the Django ASGI server, Redis, etc.) — see [cave-cli](../cave-cli/SKILL.md) for the full command reference. This skill is specifically about getting a running instance you can look at, monitor, and verify.

---

## 1. Start it

`cave run` is a long-running foreground process — run it in the background and watch its output rather than blocking on it:

```sh
cave run
```

First boot runs `manage.py check`, ensures Postgres is up, and applies DB setup/migrations — this can take noticeably longer than subsequent starts.

### Useful Flags

- `cave run <ip>:<port>`: Run on a specific LAN `ip:port` instead of localhost (uses a self-signed SSL cert — see `utils/lan_hosting/readme.md`).
- `cave run --all`: Disables the terminal TUI dashboard and streams raw container stdout/stderr.
- `cave run -it`: Run in interactive mode with the entrypoint set to bash.
- `--log-history` / `--no-log-history`: Enable or disable writing rotating server logs to `run.log` (enabled by default).
- `--log-lines <LINES>`: Maximum lines of server logs to maintain in `run.log` (default: 500).

---

## 2. Confirm it's actually serving

Poll the base URL rather than trusting the log stream — the container can report as running before Django finishes its startup checks. On first boot (waiting for Postgres, `manage.py check`, DB migrations), startup can take 45–60 seconds:

```sh
timeout 60 bash -c 'until curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/cave/ | grep -q 200; do sleep 3; done'
```

If it never comes up within that window, don't keep waiting or retry silently:
1. Scan for errors using `cave logs -e` or `cave logs -n 50`.
2. Notify the user that startup is stuck with the error snippet.
3. Run `cave kill` to stop it rather than leaving a hung container running.

---

## 3. Server Logs & Monitoring (`cave logs`)

While `cave run` is active, it maintains a rotating log file. Inspect logs without interrupting the server:

| Action | Command | Purpose |
|---|---|---|
| Scan errors & exceptions | `cave logs -e` | Shows only errors/exceptions. Best for token efficiency. |
| Scan errors & warnings | `cave logs -e -w` | Shows errors plus warning logs. |
| Tail recent activity | `cave logs -n 20` | Shows the last 20 log lines. |
| Stream logs in real time | `cave logs -f` | Follow live activity (`Ctrl+C` to detach). |
| Get log file path | `cave logs -p` | Prints absolute path to `run.log`. |
| Clear server log | `cave logs -c` | Clears `run.log` before reproducing an issue. |

---

## 4. Open and drive it

The app lives at `http://localhost:8000/cave/` — Chrome is the only fully supported browser.

- Most of the app requires being logged in. The default admin's credentials are in this project's `.env` (`DJANGO_ADMIN_USERNAME` / `DJANGO_ADMIN_PASSWORD`) — treat `.env` as a secrets file: look up a specific key if you need it, don't cat/print/paste its full contents into chat or logs.
- After login, click the app-page icon, then the examples switcher (three sliders, top left) to browse the bundled `cave_api/examples/` — see the [examples](../examples/SKILL.md) skill.
- A blank/grey screen after load means a frontend error, not necessarily a Python one — see the [debug](../debug/SKILL.md) skill (start with the browser console, `Ctrl+Shift+i`).

`cave prettify && cave test init.py` (see [lint](../lint/SKILL.md) and [test](../test/SKILL.md)) validates your `execute_command` output headlessly and is faster for iterating on API changes. Reach for a real run when you need to see the rendered UI itself, not just validate the schema. Note that `cave test` runs in a separate test environment and can run concurrently while `cave run` is actively serving.

---

## 5. Stop it

`cave kill` stops the containers — it's in the destructive tier of [cave-cli](../cave-cli/SKILL.md), so confirm with the user before running it. The one exception is the stuck-startup case in step 2: there, notifying the user *is* the confirmation — kill it right after telling them, don't leave a hung container running while waiting on a reply.
