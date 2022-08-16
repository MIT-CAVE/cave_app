# Cave App
A Django server to act as a Cave Back End

# Getting Started

## Development Prerequisites

- Make sure you are using a Unix based kernel (Mac or Linux).
  - If you are using Windows, you can use Ubuntu20.04 (via WSL2).
    - While using WSL2, make sure to follow all instructions in your WSL2 terminal
- Install Python 3.9.x (or higher) python pip and python dev tools
  - Note: Only python is supported (and not derivatives like anaconda)
  - You can download python [here](https://www.python.org/downloads/).
- Install Postgres:
  - On Ubuntu:
    ```sh
    sudo apt-get install postgresql
    sudo apt-get install postgresql-contrib
    ```
  - On Mac (via Brew):
    ```sh
    brew install postgresql
    brew services start posgresql
    ```

## CLI Instructions

1. Install the CLI:
    ```
    bash -c "$(curl https://raw.githubusercontent.com/MIT-CAVE/cave_cli/main/install.sh)"
    ```
    - Validate Installation:
      ```
      cave --version
      ```
    - Get cli help:
      ```
      cave --help
      ```

2. Create a new cave app:
    ```
    cave create my_app
    ```

3. Enter the app:
    ```
    cd my_app
    ```

4. Run the app at `localhost:3000` (while in `my_app`):
    ```
    cave run
    ```

## Standard Instructions

1. Clone this repo in your preferred directory and enter the repo:
    ```
    git clone git@github.com:MIT-CAVE/cave_app.git
    cd cave_app
    ```

2. Setup a virtual environment and install all requirements:
    Install (or upgrade) virtualenv:
    ```
    python3 -m pip install --upgrade virtualenv
    ```
    Create your virtualenv named `venv`:
    ```
    python3 -m virtualenv venv
    ```
    Activate your virtual environment on Unix (Mac or Linux):
    ```
    source venv/bin/activate
    ```
    Install all requirements for development:
    ```
    pip install -r requirements.txt
    ```

## Update the Server Environment Variables

1. Rename `example.env` to `.env`
  ```
  mv example.env .env
  ```
2. Update the `.env` file
  - Make sure to edit:
    - `SECRET_KEY`: A [Django SECRET_KEY](https://docs.djangoproject.com/en/4.1/ref/settings/#secret-key)
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
          - EG: `STATIC_APP_URL_PATH='0.0.1/index.html'`
3. Open `.gitignore` and remove `.env` (if you wish to commit .env changes to your source control)


## Mapbox Setup

1. Go to [mapbox.com](https://mapbox.com) and create an account.
2. Copy your public token to `MAPBOX_TOKEN` in your `.env` file.


## Local Deployment

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
  - Optional: Run the app on `<your-ip>:8000` with development settings:
    ```
    python manage.py runserver <your-ip>:8000
    ```

  - Optional: Run the app on `<any-ip>:8000` that points to your machine with development settings:
    ```
    python manage.py runserver 0.0.0.0:8000
    ```

## Admin Access
1. Login as:
  - See the admin information that you set in the `./.env` file.

2. To view the admin page navigate to: `localhost:8000/admin`

## Making API Changes
See the API documentation
- [General API Topics](cave_api/README.md)
- [API Structure](cave_api/README_API_STRUCTURE.md)

# Prettify Code
NOTE: All prettify commands write over existing code.

To apply our default lint fixes to all python code in `./cave_core` and `./cave_app`:
```
./utils/prettify.sh
```

To apply our default lint fixes to all python code in `./cave_api`:
```
./utils/api_prettify.sh
```
