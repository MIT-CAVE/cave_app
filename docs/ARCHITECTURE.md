# CAVE App — Architecture Overview

This page gives a high level view of a CAVE app: the projects it depends on, how it is deployed, how its code is organized, and what it offers to its users. It is intended for app developers first, and for anyone deploying or evaluating a CAVE app.

---

## Ecosystem

| Project | What it is | Deployed? |
|---|---|---|
| **cave_app** | This repository: the Django server, admin interface, and the `cave_api` folder where your app logic lives. Used as a template for every new app. | Yes |
| **cave_static** | A static React build that browsers load to render the app UI. Hosted on a CDN. | Loaded by the browser |
| **cave_utils** | A Python package with validation, logging, and builder utilities. Installed via `pyproject.toml`. | Yes (as a dependency) |
| **cave_cli** | The command-line tool used to create, run, test, and manage apps during development. | No |

```mermaid
flowchart LR
    dev([App developer]) -->|cave create / run / test| cli[cave_cli]
    cli -->|clones template, runs Docker| app[cave_app<br/>+ your cave_api]
    utils[cave_utils] -->|Python dependency| app
    user([End user / admin]) -->|browser| static[cave_static<br/>React UI, from CDN]
    static <-->|HTTP + WebSocket| app
```

---

## Deployment

Each app runs as a set of Docker containers on a dedicated network. `cave run` starts them for you (see the [Cave CLI](https://github.com/MIT-CAVE/cave_cli)); see [NON_CLI_README.md](NON_CLI_README.md) to run them manually or in production.

| Container | Image | Purpose |
|---|---|---|
| `<app>_django` | built from this `Dockerfile` | Django server (ASGI, via uvicorn), serving HTTP and WebSocket traffic |
| `<app>_db_host` | `postgres` | Database: users, groups, teams, site content, sessions |
| `<app>_redis_host` | `valkey/valkey` | Cache for session data and message broker for WebSocket broadcasts |
| `<app>_nginx_host` | `nginx` | Optional HTTPS reverse proxy, used for LAN hosting |

```mermaid
flowchart LR
    browser([Browser]) -->|http://localhost:8000| django
    browser -.->|https://ip:port<br/>LAN hosting only| nginx[nginx]
    nginx -.-> django
    subgraph net [Docker network]
        django[Django<br/>uvicorn] --> db[(PostgreSQL)]
        django --> cache[(Valkey / Redis)]
    end
    db --- pgvol[/pg volume/]
    cache --- redisvol[/redis volume/]
```

---

## Components and Data Flow

| Folder | Role | Who touches it |
|---|---|---|
| `cave_api/` | Your app logic, exposed through `execute_command` | You, almost always |
| `cave_core/` | Django app: models, auth, views, WebSocket session logic | Rarely |
| `cave_app/` | Django project: settings, ASGI, URL routing | Rarely |

See [DEVELOPMENT.md](DEVELOPMENT.md) for the full project structure.

When a user interacts with the UI, the request goes through the WebSocket layer to your `execute_command` function, and the returned `session_data` is broadcast back to every window and user in the same session:

```mermaid
sequenceDiagram
    participant UI as Browser (cave_static)
    participant WS as cave_core (WebSockets)
    participant API as cave_api (execute_command)
    participant C as Valkey / Redis
    UI->>WS: command (e.g. "init", button click)
    WS->>C: load session_data
    WS->>API: execute_command(session_data, socket, command)
    API-->>WS: updated session_data
    WS->>C: store session_data
    WS-->>UI: broadcast changes to all session members
```

See [API_README.md](API_README.md) for details on `execute_command`.

---

## Capabilities

| For | What the app provides |
|---|---|
| **End users** | Interactive maps, charts and dashboards, KPI panels, input panes (sliders, dropdowns, toggles, ...), multi-command workflows, and synchronized multi-window / multi-user sessions |
| **Admins** | Content pages editable from the app, and management of accounts, access, groups, and teams via the admin interface (`/cave/admin`) |
| **App developers** | A single Python entry point (`execute_command`); no frontend or backend code to write |
