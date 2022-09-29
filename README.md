# Cave App
A Django server to host the API and act as the Cave back end.

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

![login page](https://utils.mitcave.com/docs/cave_app-0.3.0/login.png)
You should now see the above page displayed. You can log in by clicking the top right button on the screen, and entering your login information.

## Login as Admin
1. Use the admin information that you used during setup, or look in the `.env` file in the root of this directory).

2. To view the admin page navigate to: `localhost:8000/admin`
![admin page](https://utils.mitcave.com/docs/cave_app-0.3.0/admin.png)
This is the automatic Django admin interface that allows you to manage all your models across the app and edit the content of the website. See [this explanation](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site#logging_in_and_using_the_site) for more information on how to use the admin interface. 

## Main Features
### Create a session
To access the main features of the CAVE app, first create a new session by clicking the fourth button on the top left corner.
<img src="https://utils.mitcave.com/docs/cave_app-0.3.0/session.png" width=50%>

Creating a new session will launch whichever model is called in `/cave_api/src/cave_api/__init__.py` file. We supply two example models for users to reference and/or build upon. In this tutorial, we will demonstrate the features of the `simple_model`, which demonstrates good practices for researchers using the CAVE API. The other model, `static_model`, contains examples of the whole API structure, and is useful for developers to debug, experiment with new features, etc. You can build on top of whichever model is more applicable to your research, or create your own model.

### Map View

Once you're in your new session, you will see the Map view.
![map view](https://utils.mitcave.com/docs/cave_app-0.3.0/map.jpg)

You can click on each of the warehouses and factories to toggle open, and click the lightning bolt button on the left sidebar to calculate the statistics and KPI of the model. 

<img src="https://utils.mitcave.com/docs/cave_app-0.3.0/map1.png" width=50%>


### Dashboard View
Click the lower right buttons on the left sidebar to toggle between Map, Dashboard, and KPI view. In the Dashboard view, you can generate charts based on the statistics and KPI of the model. You can adjust various elements of the charts, such as type of chart, statistic, groupings, etc.
![dashboard view](https://utils.mitcave.com/docs/cave_app-0.3.0/dashboard.jpg)

### KPI View
In KPI view, you can see the list of all the KPI and their values. 
![kpi view](https://utils.mitcave.com/docs/cave_app-0.3.0/kpi.jpg)

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
- Connor Makowski - CAVE Researcher / Project Manager / Developer
- Tim Russell - CAVE Researcher
- Matthias Winkenbach - CAVE Director

## License Notice

Copyright 2022 Massachusetts Institute of Technology (MIT), Center for Transportation & Logistics (CTL)

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
