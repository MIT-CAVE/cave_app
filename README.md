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

        - Example on ip `192.168.1.00` with port `8000`:
          ```
          cave run 192.168.1.100:8000
          ```
        - Example for a wildcard ip (any network ip that routes to your machine):
          ```
          cave run 0.0.0.0:8000
          ```
        - Note: This requires one free port above the specified port to run the server
        - Note: When LAN hosting, an SSL connection is required. The `cave_cli` does this automatically, however there are a few caveats:
            - This uses a self signed and insecure certificate for SSL/TLS reasons
            - The certificates are self signed and shared openly in the cave open source project
            - You should consider appropriate security measures like generating your own SSL certificates and using a proper CA (certificate authority) if you do not trust everyone on your LAN
        - Note: When LAN hosting, a production `daphne` server is started. This requires proper static file serving. To achieve this, `cave_cli` will automatically `collectstatic` when a specific ip and port are provided
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
  - You can create unique user experiences quickly using the CAVE API
    - EG: [Adding buttons to the `appBar`](/cave_api/docs/all_keys/app_bar.md)
  - This contains built in session management for synchronous multi window or multi user access
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
To fully understand how the cave app works, it is best to dive into our default example application.

- Ensure the app is running:
  ```
  cave run
  ```
- Login (or create an account)
  - For example purposes, we recommend you login as the default admin
    - Use the info from when you created the cave app.
    - This can also be found in `your_app/.env`
  - The login button appears in the main app bar (or menu if on mobile)
- Create a session:
  - Click on the app page icon (A square with spaces along its edges)
  - This will show your current sessions and allow you to create new sessions
    <details>
    <summary>Example image</summary>
    <img src="https://utils.mitcave.com/docs/cave_app-0.3.0/session.png" width=50%>
    </details>
  - Creating a new session will initialize whichever model is specified in the `/cave_api/src/cave_api/__init__.py` file
    - We supply multiple example models for users to reference and/or build upon.
      - The `simple_model` demonstrates good practices for researchers using the CAVE API
      - The `static_model` contains examples of the whole API structure, and is useful for developers to debug and experiment with new features
      - You can build on top of whichever model is more applicable to your research, or create your own model

  <details>
  <summary>Simple Model Walk Through</summary>

    - You can customize the interactive data you want to render in your model, and display them in three types of views
      - Map View
      - Dashboard View
      - KPI View.
    - In the `simple_model`, we render the following Map view. You can click on each of the warehouses and factories to toggle open and calculate the statistics and KPI of the model.
    ![map view](https://utils.mitcave.com/docs/cave_app-0.3.0/map.jpg)

    - In the `simple_model` Dashboard view, you can generate charts based on the statistics and KPI of the model. You can adjust various elements of the charts, such as type of chart, statistic, groupings, etc.
    ![dashboard view](https://utils.mitcave.com/docs/cave_app-0.3.0/dashboard.jpg)

    - In the `simple_model` KPI view, you can see the list of all the KPI and their values.
    ![kpi view](https://utils.mitcave.com/docs/cave_app-0.3.0/kpi.jpg)

    - These functions are all programmed in `/cave_api/src/cave_api/simple_model`. The CAVE [API Structure](cave_api/README_API_STRUCTURE.md) gives developers many capabilities to edit and create their own models. For instance, you can [change levels of data aggregation](/cave_api/docs/all_keys/categories.md) in Dashboard view or [edit the map legend](/cave_api/docs/all_keys/arcs.md) displayed in Map view.

  </details>


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

## Project Contributors

- Willem Guter - CAVE Developer
- Luis Vasquez - CAVE Developer
- Erin Liu - CAVE Developer
- Jean Billa - CAVE Developer
- Connor Makowski - CAVE Researcher / Project Manager / Developer
- Tim Russell - CAVE Researcher
- Matthias Winkenbach - CAVE Director

## License Notice

Copyright 2022 Massachusetts Institute of Technology (MIT), Center for Transportation & Logistics (CTL)

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
