# Cave App
Quickly create interactive web applications for python based models.
![map view](https://utils.mitcave.com/docs/cave_app-0.3.0/map.jpg)

# Getting Started

1. Install the [Cave CLI](https://github.com/MIT-CAVE/cave_cli). See the full instructions how how to install the Cave CLI [here](https://github.com/MIT-CAVE/cave_cli).
    - If you do not want to use the CLI (or for production deployments), see the instructions [here](NON_CLI_README.md).

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
          - Access with `https://192.168.1.100:8000`
        - Note: When LAN hosting, an SSL connection is required. The `cave_cli` does this automatically, however there are a few caveats:
            - This uses a self signed and insecure certificate for SSL/TLS reasons
            - The certificates are self signed and shared openly in the cave open source project
            - You should consider appropriate security measures like generating your own SSL certificates and using a proper CA (certificate authority) if you do not trust everyone on your LAN
    </details>

5. In Chrome, you can now open the web app:
    - EG: If you use the standard settings
    ```
    http://localhost:8000
    ```

## Cave App Components
The cave app includes a variety of core components to allow for rapid prototyping, development and testing. The main components include:

- Customizable web pages that allow for creating and modifying simple information based web content on the fly
  - Managed by a simple admin interface after deployment
  - Content scales seamlessly between mobile and desktop


- Interactive Application
  - This contains built in session management for synchronous multi window and multi user experiences
  - See the [Cave API folder](/cave_api) for step-by-step details on how to get started on API development with the CAVE App.


- Admin features to control accounts, access, groups, teams, site content and more
  <details>
  <summary>Admin Getting Started</summary>

  1. Login using the admin information that you used during setup, or look in the `.env` file in the root of your app directory).

  2. To view the admin page navigate to: `localhost:8000/admin`
  ![admin page](https://utils.mitcave.com/docs/cave_app-0.3.0/admin.png)

  3. From the Admin page, you can add pages and content to your website
    - The following content types are supported: photos, videos, breaks, headers, HTML content, quotes, resources, and FAQs
    - As an example, a created page can look like:
    ![example page](https://utils.mitcave.com/docs/cave_app-0.3.0/example_page.png)
  </details>

## Using The Example App
To fully understand how the cave app works, it is best to dive into some of our examples. The cave app comes with pre-built examples to help you understand all the components you can take advantage of and how to use them. To use the example app, follow the steps below:

- Ensure the app is running:
  ```
  cave run
  ```
- Login (or create an account)
  - For example purposes, we recommend you login as the default admin
    - Use the info from when you created the cave app.
    - This can also be found in `your_app/.env`
  - The login button appears in the main app bar
- Click on the app page icon (A square with spaces along its edges)
- We supply multiple example code structures for you to use for reference and to build on top of. You can find them in `/cave_api/cave_api/examples`
  - By default, you will get an app with a button (three sliders) in the top left corner that allows you to switch between all of our examples. 
  - Click on the three sliders to open the example menu and choose an example to view.
  - To see the code for each example, navigate to `your_app/cave_api/cave_api/examples` and open the example you want to view.


## Making API Changes
See the API documentation:

- [General API Topics](cave_api/README.md)
- [API Spec](https://mit-cave.github.io/cave_utils/cave_utils/api.html)

### Prettify Code
Use the CLI to keep your API code `pretty` and match CAVE coding format standards.

  ```sh
  cave prettify
  ```

**NOTE**: All prettify commands write over existing code (in place).

## Project Contributors

- Willem Guter - CAVE Developer
- Luis Vasquez - CAVE Developer
- Alice Zhao - CAVE Developer
- Max Katz-Christy - CAVE Developer
- Elaine Wang - CAVE Developer
- Tim Russell - CAVE Researcher
- Connor Makowski - CAVE Researcher / Development Lead
- Matthias Winkenbach - CAVE Director

## Previous Contributors
- Robert Tran - CAVE Developer
- Yang Dai - CAVE Developer
- Margaret Sands - CAVE Developer
- Kristen Manning - CAVE Developer
- Alan Yan - CAVE Developer
- Chris Larry - CAVE Developer
- Chloe Wang - CAVE Developer
- Shepherd Jiang - CAVE Developer
- Samip Jain - CAVE Developer
- Erin Liu - CAVE Developer
- Sanjay Seshan - CAVE Developer
- Jean Billa - CAVE Developer
- Austin Lee - Conarrative Developer
- Alex Dixon - Conarrative Developer
- Steven Achstein - Conarrative Developer
- Mike Gai - Conarrative Developer

## License Notice

Copyright 2023 Massachusetts Institute of Technology (MIT), Center for Transportation & Logistics (CTL)

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
