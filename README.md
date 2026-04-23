# Cave App

Cave App is an open-source framework for rapidly building interactive web applications on top of Python models and data pipelines. It handles the full stack: web server, real-time session management, admin interface, and a React-based frontend. You can focus entirely on your Python logic. It is designed for researchers, data scientists, and engineers who want to turn models into shareable, interactive tools without writing frontend or backend code.

Click the image below to see a video introduction to the cave app:

[![cave app intro](https://img.youtube.com/vi/-wWrNW8qG18/maxresdefault.jpg)](https://youtu.be/-wWrNW8qG18)

# Prerequisites

Before getting started, ensure you have the following installed:

- [Google Chrome](https://www.google.com/chrome/): the only fully supported browser
- [Docker](https://www.docker.com/get-started/): required to run the app locally
- [Python 3](https://www.python.org/downloads/): required for the Cave CLI
- [Cave CLI](https://github.com/MIT-CAVE/cave_cli): the command-line tool used to create and run apps

# Getting Started

1. Install the [Cave CLI](https://github.com/MIT-CAVE/cave_cli).
    - If you do not want to use the CLI (or for production deployments), see the instructions [here](NON_CLI_README.md).

2. Create a new cave app (replace `my_app` with your desired app name):
    ```
    cave create my_app
    ```

3. Enter the app:
    ```
    cd my_app
    ```

4. Run the app at `localhost:8000/cave/` (while in the directory `my_app`):
    ```
    cave run
    ```
    <details>
    <summary>More hosting options</summary>

    - Optional: Run the app on `<your-ip>:<your-port>` with development settings:
        ```
        cave run <your-ip>:<your-port>
        ```
        - Access with `https://<your-ip>:<your-port>`
        - Example on ip `192.168.1.100` with port `8000`:
          ```
          cave run 192.168.1.100:8000
          ```
          - Access with `https://192.168.1.100:8000/cave/`
        - Note: When LAN hosting, an SSL connection is required. The `cave_cli` does this automatically, however there are a few caveats:
            - This uses a self signed and insecure certificate for SSL/TLS reasons
              - The included certificates are self signed and shared openly in the cave open source project
              - You should consider appropriate security measures like generating your own SSL certificates
              - See the [Cave App SSL/TLS documentation](utils/lan_hosting/readme.md) for more information on how to set up your own SSL certificates and integrate them with the cave app.
    </details>

5. In Chrome, open the web app:
    ```
    http://localhost:8000/cave/
    ```

## Using The Example App

To fully understand how the cave app works, it is best to dive into some of our examples. The cave app comes with pre-built examples to help you understand all the components you can take advantage of and how to use them.

Once your app is running (see [Getting Started](#getting-started) above) and you have opened it in Chrome:

- Login (or create an account)
  - For example purposes, we recommend you login as the default admin
    - Use the info from when you created the cave app.
    - This can also be found in `my_app/.env`
  - The login button appears in the main app bar
- Click on the app page icon (a square with spaces along its edges)
- By default, you will see a button (three sliders) in the top left corner that allows you to switch between all of our examples.
  - Click on the three sliders to open the example menu and choose an example to view.
  - To see the code for each example, navigate to `my_app/cave_api/cave_api/examples` and open the example you want to view.

## Making API Changes

The `cave_api` is where you integrate your own Python models, data, and logic into the app. You expose functionality through a simple `execute_command` function, and the Cave App handles the rest: routing commands, managing sessions, and updating the frontend in real time.

See the API documentation to get started:

- [General API Topics](cave_api/README.md)
- [API Spec](https://mit-cave.github.io/cave_utils/cave_utils/api.html)

## Development Workflow

### Prettify Code

Use the CLI to keep your API code formatted and consistent with CAVE coding standards:

```sh
cave prettify
```

**NOTE**: All prettify commands write over existing code (in place).

## Cave App Components

The cave app includes a variety of core components to allow for rapid prototyping, development and testing. The main components include:

- Customizable web pages that allow for creating and modifying simple information based web content on the fly
  - Managed by a simple admin interface after deployment
  - Content scales seamlessly between mobile and desktop
  - When logged in as an admin, you can browse and edit pages by clicking on the admin icon in the top right corner of the app next to the logout button.


- Interactive Application
  - This contains built in session management for synchronous multi window and multi user experiences
  - See the [Cave API folder](/cave_api) for step-by-step details on how to get started on API development with the CAVE App.


- Admin features to control accounts, access, groups, teams, site content and more
  <details>
  <summary>Admin Getting Started</summary>

  1. Login using the admin information that you used during setup, or look in the `.env` file in the root of your app directory.

  2. To view the admin page navigate to: `localhost:8000/cave/admin`

  3. From the Admin page, you can add pages and content to your website
    - The following content types are supported: photos, videos, breaks, headers, HTML content, quotes, resources, and FAQs
  </details>

## License Notice

Copyright 2025 Massachusetts Institute of Technology (MIT), Center for Transportation & Logistics (CTL)

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
