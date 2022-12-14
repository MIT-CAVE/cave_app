## Non CLI Setup Instructions
1. Install the [Cave Development Prerequisites](https://github.com/MIT-CAVE/cave_cli#development-prerequisites)

2. Clone this repo in your preferred directory and enter the repo:
    ```
    git clone git@github.com:MIT-CAVE/cave_app.git
    cd cave_app
    ```

3. Setup a virtual environment and install all requirements:

    - Install (or upgrade) virtualenv:
        ```
        python3 -m pip install --upgrade virtualenv
        ```
    - Create your virtualenv named `venv`:
        ```
        python3 -m virtualenv venv
        ```
    - Activate your virtual environment on Unix (Mac or Linux):
        ```
        source venv/bin/activate
        ```
    - Install all requirements for development:
        ```
        pip install --require-virtualenv -r requirements.txt
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
        - `DATABASE_NAME`: The name of your locally hosted development database in postgresql
            - NOTE: Certain features wipe the database so you should have a unique `DATABASE_NAME` per project
        - `DATABASE_USER`: A user to access your database
            - NOTE: You should have a unique `DATABASE_USER` per project to avoid password change conflicts
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

1. Remove any legacy database (if it exists) and set up the stock database:
    ```
    cd path/to/cave_app
    sudo chmod 700 .
    ./utils/reset_db.sh
    ```
2. Run the app on `localhost:8000` with development settings:
    ```
    python manage.py runserver
    ```
3. Run the app on a LAN (local area network):
    - Note: To run on LAN, you must use an SSL connection.
    - Note: This uses a self signed and insecure certificate for SSL/TLS reasons
        - The certificates are self signed and shared openly in the cave open source project
        - You should consider appropriate security measures like generating your own SSL certificates and using a proper CA (certificate authority) if you do not trust everyone on your LAN
    - Note: This uses the `daphne` production server.
        - You will need to `collectstatic` in order for your staticfiles to load properly.
        ```
        python manage.py collectstatic
        ```
    - To run the server:
    ```
    daphne -e ssl:8000:privateKey=utils/lan_hosting/LAN.key:certKey=utils/lan_hosting/LAN.crt cave_app.asgi:application -p 8001 -b 0.0.0.0
    ```
        - Note: You will need to access the app from the ssl port (in the above case `8000`) and not the port specified by `-p`.
        - Note: You can specify the LAN IP with
            - Wildcard: `-b 0.0.0.0`
                - This allows you to access the sever from any IP that points to your machine
            - Specific: `-b 192.168.1.100`
                - Note: Replace `192.168.1.100` with your local IP address
                - This allows you to access the sever from a specific IP that points to your machine
    - To access the server go to:
    ```
    https://192.168.1.100:8000
    ```
      - Note: Replace `192.168.1.100` with your local IP address


### Prettify Code
NOTE: All prettify commands write over existing code.

To apply our default lint fixes to all python code in `./cave_core` and `./cave_app`:
```
./utils/prettify.sh
```

To apply our default lint fixes to all python code in `./cave_api`:
```
./utils/api_prettify.sh
```
