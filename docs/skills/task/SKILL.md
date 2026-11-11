---
name: task
description: Inspect, schedule, attach to, cancel, and manage background tasks and the task runner via the cave CLI (cave task). Use when managing task queues, running background tasks/tests/prettify, viewing task logs, or stopping/resetting the task runner.
---

# Managing Tasks & The Task Runner

The CAVE CLI uses a dedicated task runner container environment to execute tasks sequentially in the background. This environment runs independently of the live dev server (`cave run`), so tasks and tests never cause container or port conflicts with an active browser session.

Automated tests (`cave test`) and code formatting (`cave prettify`) submit work directly into this task queue. You can also submit arbitrary commands and scripts using `cave task start`.

---

## Attached vs. Detached Execution

- **Attached (Default)**: Running `cave test <file>`, `cave prettify`, or `cave task start <command>` attaches to the task output immediately and streams logs until completion.
- **Detached (`-d` / `--detached`)**: Add `-d` to any task command to run it in the background without blocking your terminal:
  ```sh
  cave test init.py -d
  cave prettify -d
  cave task start "python manage.py migrate" -d
  ```

### Interactive Controls While Attached

When attached to a running task (either initially or via `cave task attach`):
- `Esc`: Detach from task and return to terminal (task continues running in the background).
- `Ctrl+C`: Cancel and terminate the task.

---

## Non-Interactive Log Inspection (`cave logs -t`)

For token-efficient workflows, automated scripts, or checking task output without entering an interactive terminal session, use `cave logs -t`:

```sh
# Inspect output of the latest task:
cave logs -t

# Limit output to the last 50 lines (recommended for agents):
cave logs -t -n 50

# Inspect output of a specific task ID:
cave logs -t 4 -n 50
```

---

## Command Reference

`cave task` provides subcommands along with convenient top-level flag shortcuts:

| Subcommand | Flag Shortcut | Description |
|---|---|---|
| `cave task start <cmd>` (or `run`) | — | Schedule and run arbitrary files or container commands sequentially (supports `-d`, `--docker-args`) |
| `cave task list` (or `ls`) | `cave task -l` (or `cave task`) | Display active tasks in the queue with incremental IDs, status, and duration |
| `cave task list-all` (or `la`) | `cave task -la` | Display all recorded tasks (active, completed, failed, and cancelled) |
| `cave task list-all -n <N>` | `cave task -la -n <N>` | Limit task list output to the last N tasks (saves tokens) |
| `cave task attach [ID]` (or `join`, `log`, `logs`) | `cave task -a [ID]` | Reattach to a queued or running task to view live streaming logs (defaults to current active task) |
| `cave task clean` (or `clear`) | `cave task --clean` | Clean completed task logs and remove completed tasks from registry |
| `cave task kill <ID>` (or `cancel`) | `cave task -k <ID>` | Cancel a queued task or terminate a running task container by incremental ID |
| `cave task kill-all` (or `cancel-all`) | `cave task --kill-all` | Cancel all queued and running tasks |
| `cave task stop` (or `kill-server`) | `cave task --stop` | Stop task server containers and clean up completed task logs (also available via `cave kill -t`) |
| `cave task reset` | `cave task --reset` | Tear down the task server, remove database/redis volumes, rebuild container image, and reset task registry |

---

## Common Workflows

### 1. Run a detached test and inspect output efficiently

```sh
# 1. Format code before testing
cave prettify -d

# 2. Run test in the background
cave test init.py -d

# 3. Check queue and task status
cave task -la -n 5

# 4. Inspect test output non-interactively without unbounded log dump
cave logs -t -n 50
```

### 2. View recent task history without token bloat

```sh
# Display only the last 5 or 10 tasks:
cave task -la -n 10
```

### 3. Attach interactively to a long-running task

```sh
# Attach to live stream
cave task attach

# While attached:
# Press Esc to detach (leaves task running)
# Press Ctrl+C to cancel and terminate task
```

### 4. Schedule a custom task or command

```sh
# Run a custom script inside the task container in detached mode:
cave task start "python tests/test_custom.py" -d

# Check log output:
cave logs -t -n 50
```

### 5. Clean up old task logs

```sh
# Clean completed logs and tidy the registry
cave task clean
```

### 6. Cancel tasks

```sh
# Cancel a specific task by its ID
cave task kill 2

# Cancel all active and queued tasks
cave task kill-all
```

### 7. Stop or Reset the Task Server

```sh
# Stop the background task server
cave task stop

# Reset the task runner environment (after Dockerfile, dependency, or DB model changes)
cave task reset
```

---

## See Also
- [test](../test/SKILL.md) — Running automated test suites via the task runner.
- [lint](../lint/SKILL.md) — Running code formatting (`cave prettify`) via the task runner.
- [debug](../debug/SKILL.md) — Debugging server and task failures.
- [cave-cli](../cave-cli/SKILL.md) — Full CLI command reference.
