## Non CLI Setup Instructions
1. Install the [Cave Development Prerequisites](https://github.com/MIT-CAVE/cave_cli#development-prerequisites)

2. Clone this repo in your preferred directory and enter the repo:
    ```
    git clone git@github.com:MIT-CAVE/cave_app.git
    cd cave_app
    ```

3. Install Docker

    ```sh
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh ./get-docker.sh
    ```

    Add the current user to the docker group

    ```sh
    dockerd-rootless-setuptool.sh install
    ```

    Make sure it works outside of sudo

    ```sh
    docker run hello-world
    ```

### Update the Server Environment Variables

1. Rename `example.env` to `.env`
    ```
    mv example.env .env
    ```
2. Update the `.env` file
    - Make sure to edit:
        - `SECRET_KEY`: A [Django SECRET_KEY](https://docs.djangoproject.com/en/4.1/ref/settings/#secret-key)
            - If you used the CLI to create this `.env` file, a random secret key was generated during that process.
        - `DJANGO_ADMIN_EMAIL`: The email for the site administrator
        - `DJANGO_ADMIN_PASSWORD`: A secure password for the site administrator
        - `DATABASE_PASSWORD`: A secure password for database access
      - You might also consider editing:
          - `STATIC_APP_URL` and `STATIC_APP_URL_PATH`
              - If you plan doing development on `cave_static` and deploying it locally:
                  - `STATIC_APP_URL='http://localhost:3000'`
                  - `STATIC_APP_URL_PATH=''`
              - To use any existing static build:
                  - `STATIC_APP_URL='https://builds.mitcave.com'`
                  - `STATIC_APP_URL_PATH='<major>.<minor>.<patch>/index.html'`
                      - EG: `STATIC_APP_URL_PATH='0.1.0/index.html'`
3. Open `.gitignore` and remove `.env` (if you wish to commit .env changes to your source control)


### Mapbox Setup

1. Go to [mapbox.com](https://mapbox.com) and create an account.
2. Copy your public token to `MAPBOX_TOKEN` in your `.env` file.


### Local Deployment

1. Navigate to the app and build the container
    ```
    cd path/to/cave_app
    source .env
    app_name='cave_test'
    docker build . --tag cave-app:${app_name}
    ```
2. Create a Docker network for the containers to run in
    ```
    app_name='cave_test'
    docker network create cave-net:${app_name}
    ```
3. Start postgres
    ```
    source .env
    app_name='cave_test'
    docker run -d \
        --volume "${app_name}_pg_volume:/var/lib/postgresql/data" \
        --network cave-net:${app_name} \
        --name "${app_name}_db_host" \
        -e POSTGRES_PASSWORD="$DATABASE_PASSWORD" \
        -e POSTGRES_USER="${app_name}_user" \
        -e POSTGRES_DB="${app_name}_name"\
        "$DATABASE_IMAGE" $DATABASE_COMMAND
    ```
    > Note: Replace `cave_test` with the name of your app
3. Run the app on `localhost:8000` with development settings:
    ```
    source .env
    app_name='cave_test'
    docker run -it -p 8000:8000 --network cave-net:${app_name} --volume "./:/app" --volume "$CAVE_PATH:/cave_cli" --name "${app_name}_django" \
      -e DATABASE_HOST="${app_name}_db_host" \
      -e DATABASE_USER="${app_name}_user" \
      -e DATABASE_PASSWORD="$DATABASE_PASSWORD" \
      -e DATABASE_NAME="${app_name}_name"\
      -e DATABASE_PORT=5432 \
      "cave-app:${app_name}" /app/utils/run_server.sh && docker rm --force "${app_name}_django" "${app_name}_db_host"
    ```
    > Note: Replace `cave_test` with the name of your app
4. Run the app on a LAN (local area network) on `0.0.0.0:8123`:
    - Note: To run on LAN, you must use an SSL connection.
    - Note: This uses a self signed and insecure certificate for SSL/TLS reasons
        - The certificates are self signed and shared openly in the cave open source project
        - You should consider appropriate security measures like generating your own SSL certificates and using a proper CA (certificate authority) if you do not trust everyone on your LAN
    - To run the server:
        ```
        docker run -d --restart unless-stopped -p "0.0.0.0:8123:8000" --network cave-net --volume "./utils/lan_hosting:/certs" --name "${app_name}_nginx" -e CAVE_HOST="${app_name}_django" --volume "./utils/nginx_ssl.conf.template:/etc/nginx/templates/default.conf.template:ro" nginx
        ```

        ```
        docker run -it -p 8000 --network cave-net --volume "./:/app" --name "${app_name}_django" -e CSRF_TRUSTED_ORIGIN="0.0.0.0:8123" cave-app /app/utils/run_dev_server.sh
        ```
    > Note: Replace `${app_name}` with the name of your app
    - Note: You can specify the LAN IP with
        - Specific: `-p 192.168.1.100:8123`
            - Note: Replace `192.168.1.100` with your local IP address
            - This allows you to access the sever from a specific IP that points to your machine
    - To access the server go to:
    ```
    https://192.168.1.100:8123
    ```
    Or whichever local address you specified at the specified port


### Prettify Code
NOTE: All prettify commands write over existing code.

To apply our default lint fixes to all python code in `./cave_api`:
```
app_name='cave_test'
docker run --volume "./:/app" "cave-app:${app_name}" /app/utils/prettify.sh
```

To apply our default lint fixes to all python code:
```
docker run --volume "./:/app" "cave-app:${app_name}" /app/utils/prettify.sh -all
```

### Interactive Mode
To run the app in interactive mode:
```
docker run -it --volume "./:/app" "cave-app:${app_name}" bash
```
