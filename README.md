# Cave App
A Django server to host the an API and act as the Cave back end.

# Getting Started

## Development Prerequisites

- Make sure you are using a Unix based kernel (Mac or Linux).
  - If you are using Windows, you can use Ubuntu20.04 (via WSL2).
    - While using WSL2, make sure to follow all instructions in your WSL2 terminal
- Install `python3.9+`, `python3 pip`, `python development tools`, and `virtualenv`
  - **Note**: Only `python` is supported (and not python derivatives like anaconda)
  - On Ubuntu:
    ```sh
    # Update your package list and current packages
    sudo apt-get update && sudo apt-get upgrade
    # Install software to add external PPAs
    sudo apt install software-properties-common -y
    # Add the deadsnakes python PPA
    sudo add-apt-repository ppa:deadsnakes/ppa
    # Install python3.10 from the deadsnakes PPA
    sudo apt-get install python3.10
    # Install pip
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
    # Install virtualenv
    pip install virtualenv
    ```
  - On Mac (via Brew):
    - Install `python development tools`
      - Install `XCode` from the `App Store`
      - Once `XCode` is installed, install the XCode `Command Line Tools`
        - `menu` -> `preferences` -> `downloads` -> `command line tools`
    - Install `python3.9+`
      ```sh
      brew install python@3.10
      ```
    - Install `pip` and `virtualenv`:
      ```sh
      # Install pip
      curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
      # Install virtualenv
      pip install virtualenv
      ```
- Install `Postgres 12`:
  - On Ubuntu:
    ```sh
    sudo apt-get install postgresql postgresql-contrib
    ```
  - On Mac (via Brew):
    ```sh
    brew install postgresql
    brew services start posgresql
    ```

## CLI Instructions
NOTE: If you do not want to use the cave cli see the [Non CLI Instructions](NON_CLI_README.md).

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

4. Run the app at `localhost:8000` (while in `my_app`):
    ```
    cave run
    ```
    - Optional: Run the app on `<your-ip>:8000` with development settings:
      ```
      cave run <your-ip>:8000
      ```
      - Replace <your-ip> with an IP address that points to your machine

    - Optional: Run the app on `<any-ip>:8000` that points to your machine with development settings:
      ```
      cave run 0.0.0.0:8000
      ```

5. In Chrome, you can now open the web app:
  - EG: If you use the standard settings
  ```
  http://localhost:8000
  ```

## Admin Access
1. Login as:
  - Use the admin information that you used during setup (or look in the `./.env` file).

2. To view the admin page navigate to: `localhost:8000/admin`

## Making API Changes
See the API documentation:
- [General API Topics](cave_api/README.md)
- [API Structure](cave_api/README_API_STRUCTURE.md)

### Prettify Code
Use the CLI to keep your API code `pretty` and match cave coding format standards.

```sh
cave prettify
```

**NOTE**: All prettify commands write over existing code (in place).

## License Notice

Copyright 2022 Massachusetts Institute of Technology (MIT), Center for Transportation & Logistics (CTL)

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
