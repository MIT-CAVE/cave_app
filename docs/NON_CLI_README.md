## Non-CLI Setup Instructions

This guide covers manual setup without the [Cave CLI](https://github.com/MIT-CAVE/cave_cli). Use this for production deployments or when you prefer full control over the Docker orchestration.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) 23.0.6+
- [Git](https://git-scm.com/)

<details>
<summary>Ubuntu: Install Docker</summary>

```sh
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
# Add the current user to the docker group
dockerd-rootless-setuptool.sh install
# Verify it works without sudo
docker run hello-world
```

</details>

### 1. Clone the Repository

```sh
git clone git@github.com:MIT-CAVE/cave_app.git
cd cave_app
```

### 2. Configure the Environment

1. Copy the example environment file:
    ```sh
    cp example.env .env
    ```

2. Edit `.env` and set at minimum:

    | Variable | Description |
    |---|---|
    | `SECRET_KEY` | A [Django SECRET_KEY](https://docs.djangoproject.com/en/4.1/ref/settings/#secret-key) |
    | `DJANGO_ADMIN_EMAIL` | Administrator email address |
    | `DJANGO_ADMIN_FIRST_NAME` | Administrator first name |
    | `DJANGO_ADMIN_LAST_NAME` | Administrator last name |
    | `DJANGO_ADMIN_USERNAME` | Administrator username |
    | `DJANGO_ADMIN_PASSWORD` | A secure administrator password |
    | `DATABASE_PASSWORD` | A secure database password |
    | `MAPBOX_TOKEN` | Your [Mapbox](https://mapbox.com) public token |
    | `STATIC_APP_URL` | Base URL for the static React build (e.g. `https://builds.mitcave.com`) |
    | `STATIC_APP_URL_PATH` | Path to `index.html` (e.g. `3.6.0/index.html`) |

    Optional variables:

    | Variable | Default | Description |
    |---|---|---|
    | `DATABASE_IMAGE` | `postgres:latest` | PostgreSQL Docker image to use |
    | `CACHE_IMAGE` | `valkey/valkey:7` | Redis-compatible cache image to use |

3. (Optional) Remove `.env` from `.gitignore` if you want to commit it to source control.

### 3. Build the Docker Image

```sh
app_name='cave_test'
docker build . --tag cave-app:${app_name}
```

> Replace `cave_test` with your desired app name throughout these instructions.

### 4. Create a Docker Network

```sh
app_name='cave_test'
docker network create cave-net:${app_name}
```

### 5. Start the Database

```sh
source .env
app_name='cave_test'
docker run -d \
    --volume "${app_name}_pg_volume:/var/lib/postgresql/data" \
    --network "cave-net:${app_name}" \
    --name "${app_name}_db_host" \
    -e POSTGRES_PASSWORD="$DATABASE_PASSWORD" \
    -e POSTGRES_USER="${app_name}_user" \
    -e POSTGRES_DB="${app_name}_name" \
    "${DATABASE_IMAGE:-postgres:latest}" postgres -c listen_addresses=*
```

### 6. Start the Cache

```sh
app_name='cave_test'
docker run -d \
    --volume "${app_name}_redis_volume:/data" \
    --network "cave-net:${app_name}" \
    --name "${app_name}_redis_host" \
    "${CACHE_IMAGE:-valkey/valkey:7}" --save 7200 1
```

### 7. Initialize the Database (First Run Only)

On first run the database must be seeded. Skip this step if you are restarting an already-initialized app.

```sh
source .env
app_name='cave_test'
docker run -it \
    --network "cave-net:${app_name}" \
    --volume "./:/app" \
    --name "${app_name}_django_setup" \
    -e DATABASE_HOST="${app_name}_db_host" \
    -e DATABASE_USER="${app_name}_user" \
    -e DATABASE_PASSWORD="$DATABASE_PASSWORD" \
    -e DATABASE_NAME="${app_name}_name" \
    -e DATABASE_PORT=5432 \
    -e REDIS_HOST="${app_name}_redis_host" \
    -e REDIS_PORT=6379 \
    "cave-app:${app_name}" ./utils/reset_db.sh
docker rm "${app_name}_django_setup"
```

### 8. Run the App

```sh
source .env
app_name='cave_test'
docker run -it -p 8000:8000 \
    --network "cave-net:${app_name}" \
    --volume "./:/app" \
    --name "${app_name}_django" \
    -e DATABASE_HOST="${app_name}_db_host" \
    -e DATABASE_USER="${app_name}_user" \
    -e DATABASE_PASSWORD="$DATABASE_PASSWORD" \
    -e DATABASE_NAME="${app_name}_name" \
    -e DATABASE_PORT=5432 \
    -e REDIS_HOST="${app_name}_redis_host" \
    -e REDIS_PORT=6379 \
    "cave-app:${app_name}" ./utils/run_server.sh
```

Open the app in Chrome at `http://localhost:8000/cave/`.

### LAN Hosting (Optional)

To host on a local network with SSL:

> **Note:** The bundled certificates are self-signed and shared openly in this open-source project. For any non-test deployment, generate your own certificates. See `utils/lan_hosting/readme.md` for details.

```sh
source .env
app_name='cave_test'
ip='192.168.1.100'
port='8123'

# Start the Nginx reverse proxy
docker run -d \
    --restart unless-stopped \
    -p "${ip}:${port}:8000" \
    --network "cave-net:${app_name}" \
    --volume "./utils/lan_hosting:/certs" \
    --volume "./utils/nginx_ssl.conf.template:/etc/nginx/templates/default.conf.template:ro" \
    --name "${app_name}_nginx_host" \
    -e CAVE_HOST="${app_name}_django" \
    -e CAVE_PORT="${port}" \
    -e CAVE_IP="${ip}" \
    nginx

# Start Django with CSRF trusted origin
docker run -it \
    --network "cave-net:${app_name}" \
    --volume "./:/app" \
    --name "${app_name}_django" \
    -e DATABASE_HOST="${app_name}_db_host" \
    -e DATABASE_USER="${app_name}_user" \
    -e DATABASE_PASSWORD="$DATABASE_PASSWORD" \
    -e DATABASE_NAME="${app_name}_name" \
    -e DATABASE_PORT=5432 \
    -e REDIS_HOST="${app_name}_redis_host" \
    -e REDIS_PORT=6379 \
    -e CSRF_TRUSTED_ORIGIN="${ip}:${port}" \
    "cave-app:${app_name}" ./utils/run_server.sh
```

Access the app at `https://192.168.1.100:8123/cave/`.

### Prettify Code

To apply formatting to the `cave_api` Python code:

```sh
app_name='cave_test'
docker run --volume "./:/app" "cave-app:${app_name}" ./utils/prettify.sh
```

> **Note:** This writes changes in place.

### Interactive Mode

To drop into a bash shell inside the container:

```sh
app_name='cave_test'
docker run -it --volume "./:/app" "cave-app:${app_name}" bash
```
