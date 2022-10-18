# Cave App
A Django server to host the API and act as the Cave back end.
![map view](https://utils.mitcave.com/docs/cave_app-0.3.0/map.jpg)
This is the type of interactive data models that you can create with the CAVE API.

# Getting Started

1. Install the [Cave CLI](https://github.com/MIT-CAVE/cave_cli). See the full instructions how how to install the Cave CLI [here](https://github.com/MIT-CAVE/cave_cli).
    - If you do not want to use the CLI, see the instructions [here](NON_CLI_README.md).

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
        - Note: When LAN hosting, a production `daphne` server is used. This requires proper static file serving. To achieve this, `cave_cli` will automatically `collectstatic` when a specific ip and port are provided

5. In Chrome, you can now open the web app:
    - EG: If you use the standard settings
    ```
    http://localhost:8000
    ```

## Login as Admin
1. Use the admin information that you used during setup, or look in the `.env` file in the root of this directory).

2. To view the admin page navigate to: `localhost:8000/admin`
![admin page](https://utils.mitcave.com/docs/cave_app-0.3.0/admin.png)
This is the automatic Django admin interface that allows you to manage all your models across the app and edit the content of the website. See [this explanation](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site#logging_in_and_using_the_site) for more information on how to use the admin interface.

## Example App
### Adding Pages and Content
From the Admin page, you can add pages and content to your website. This following is an example of the types of content you can render, including photos, videos, breaks, headers, HTML content, quotes, resources, and FAQs.
![example page](https://utils.mitcave.com/docs/cave_app-0.3.0/example_page.png)

You can also create your own customized front-end features, like [adding buttons to the `appBar`](/cave_api/docs/all_keys/app_bar.md), by editing the API of your model. See the [Cave API](/cave_api) for step-by-step details on how to get started on API development with the CAVE App.

### Creating a session
To access the main features of the CAVE app, first create a new session. In the example app, the fourth button on the top left corner is the button that allows users to create a new session.

<img src="https://utils.mitcave.com/docs/cave_app-0.3.0/session.png" width=50%>

Creating a new session will launch whichever model is called in `/cave_api/src/cave_api/__init__.py` file. We supply two example models for users to reference and/or build upon. The `simple_model` demonstrates good practices for researchers using the CAVE API. The `static_model` contains examples of the whole API structure, and is useful for developers to debug and experiment with new features. You can build on top of whichever model is more applicable to your research, or create your own model.

### Customizing Interactive Data
You can customize the interactive data you want to render in your model, and display them in three types of views: Map View, Dashboard View, and KPI View.

In the `simple_model`, for instance, we render the following Map view. You can click on each of the warehouses and factories to toggle open and calculate the statistics and KPI of the model.
![map view](https://utils.mitcave.com/docs/cave_app-0.3.0/map.jpg)

In the `simple_model` Dashboard view, you can generate charts based on the statistics and KPI of the model. You can adjust various elements of the charts, such as type of chart, statistic, groupings, etc.
![dashboard view](https://utils.mitcave.com/docs/cave_app-0.3.0/dashboard.jpg)

In the `simple_model` KPI view, you can see the list of all the KPI and their values.
![kpi view](https://utils.mitcave.com/docs/cave_app-0.3.0/kpi.jpg)

These functions are all programmed in `/cave_api/src/cave_api/simple_model`. The CAVE [API Structure](cave_api/README_API_STRUCTURE.md) gives developers many capabilities to edit and create their own models. For instance, you can [change levels of data aggregation](/cave_api/docs/all_keys/categories.md) in Dashboard view or [edit the map legend](/cave_api/docs/all_keys/arcs.md) displayed in Map view.


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
