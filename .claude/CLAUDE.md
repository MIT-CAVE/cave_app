# CAVE Codebase Overview

The CAVE App is a framework that allows users to create and manage their own CAVE projects. 

- Users can create an app with a simple command like `cave create my_app`, which sets up a new CAVE project with the necessary structure and files.
- Once created, users can run their app using `cd my_app && cave run`, which starts the application and allows them to interact with it.
- Each cave project comes with this general structure and includes a `README.md` file that provides specific instructions and details about the project.

The codebase is organized into several directories, each serving a specific purpose:
- /: The root directory contains the main application code and configuration files for the CAVE App.
   - It includes the Dockerfile, .env file, example.env, manage.py script, README.md, and other essential files for setting up and running the application.
- /cave_api: This directory contains the main API code for created CAVE projects. 
    - It includes all the core functionality and logic for any particular CAVE project, such as handling user interactions, managing data, and implementing the specific features of the app.
    - Examples for potential APIs can be found in `cave_api/cave_api/examples/`
        - Each example is meant to convey a specific feature or set of features that can be implemented in the cave app. 
        - They are meant to be used as templates for building out your own API code in the `cave_api/cave_api/api.py` file.
        - Examples:
            - 3_by_3_charts_grouped_outputs.py: This example demonstrates how to create a dashboard with 3 by 3 charts that have grouped outputs. It showcases how to organize and display multiple charts in a grid layout, allowing for easy comparison and analysis of different data sets.
            - api_command_export.py: This example illustrates how to export the current API state using a button that fires a commmand.
            - api_command.py: This example demonstrates how to create a custom API command that can be triggered from the frontend. It shows how to define the command in the backend and how to call it from the frontend, allowing for custom interactions and functionality within the CAVE app.
            - chart_global_outputs.py: This example shows how to create charts with global outputs (like KPIs) that can be shared across multiple charts and components in the app. It demonstrates how to define global outputs and use them to create dynamic and interconnected visualizations.
            - chart_grouped_outputs_builder_date.py: This example illustrates how to create charts with grouped outputs that are built using date-based data. It demonstrates how to group data points based on dates and display them in a cohesive manner for better insights and analysis.
            - chart_grouped_outputs_builder.py: This example demonstrates how to create charts with grouped outputs that are built using our group builder function. It shows how to use the group builder to organize related data points together and display them in a cohesive manner for better insights.
            - chart_grouped_outputs_date.py: This example illustrates how to create charts with grouped outputs that are based on date data. It demonstrates how to group data points based on dates and display them in a cohesive manner for better insights and analysis.
            - chart_grouped_outputs.py: This example illustrates how to create charts with grouped outputs, which allows for the visualization of multiple data series within a single chart. It demonstrates how to group related data points together and display them in a cohesive manner for better insights.
            - data_external_example.py: This example demonstrates how to integrate external data sources into the CAVE app. It shows how to fetch data from an external API or database and use it to populate charts, tables, or other components within the app.
            - data_local_example.py: This example illustrates how to use local data within the CAVE app. It demonstrates how to define and manage local data sets, and how to use that data to create charts, tables, or other components within the app without relying on external data sources.
            - general_props_all.py: This example shows all the available props (interactive UI Components) that can be used in the cave app. It serves as a reference for developers to understand the different UI components they can utilize when building their own CAVE projects.
            - general_props_all_advanced.py: This example builds on the previous one by showing all the available props with more advanced configurations and use cases. It provides developers with a deeper understanding of how to use the various UI components in more complex and customized ways within their CAVE projects.
            - general_settings_sync.py: This example demonstrates how to synchronize various data states across user sessions.
            - kitchen_sink.py: This example is a comprehensive demonstration of a wide variety of features and components available in the CAVE app. It serves as a "kitchen sink" example that showcases many different functionalities and use cases in one place, providing developers with inspiration and guidance for building their own CAVE projects.
            - map.py: This example illustrates how to create a map visualization within the CAVE app. It demonstrates how to integrate mapping libraries, plot data points on a map, and customize the map's appearance and interactivity to create a dynamic and informative map-based visualization.
            - map_arcs.py: This example demonstrates how to create arc visualizations on a map within the CAVE app. It shows how to plot arcs between different locations on a map, which can be used to represent connections, flows, or relationships between those locations in a visually compelling way.
            - map_customized.py: This example illustrates how to create a customized map within the CAVE app. This customization focuses on the map visual effects instead of represented data.
            - map_custom_tiles.py: This example demonstrates how to use custom map tiles in a map visualization within the CAVE app. It shows how to integrate custom tile providers and use them to create unique and visually appealing map backgrounds for your visualizations.
            - map_geos.py: This example illustrates how to create geos (geographic areas represnted as shapes) on a map within the CAVE app. It demonstrates how to define and plot geos based on geographic data, allowing for the visualization of regions, zones, or other geographic areas on a map.
            - map_nodes.py: This example demonstrates how to create node visualizations on a map within the CAVE app. It shows how to plot nodes (points of interest) on a map, which can be used to represent locations, events, or other significant points in a visually compelling way.
            - pane_modal.py: This example illustrates how to create a modal pane within the CAVE app. It demonstrates how to design and implement a pane that appears like a modal dialog, allowing for the display of additional information, forms, or interactive content in a way that overlays the main app interface.
            - pane_wall.py: This example demonstrates how to create a wall pane within the CAVE app. It shows how to design and implement a pane that appears like a wall, which can be used to display information, visualizations, or interactive content in a way that is integrated into the main app interface without overlaying it like a modal.
    - The default application uses the `cave_api/cave_api/api.py` file which acts as a selector for each example in the `cave_api/cave_api/examples/` directory.
    - There is also a `README.md` file that is specific for `cave_api` which provides instructions and details about the API code and how to use it effectively.
    - Full api docs can be found at https://mit-cave.github.io/cave_utils/cave_utils/api.html
- /cave_app: This directory contains basic settings, asgi setup, storage_backends, and urls that are needed by Django projects to operate.
- /cave_core: This directory contains the core logic for running and operating a cave project such as:
    - `admin_forms.py`: This file contains the forms used in the Django admin interface for managing CAVE projects. These forms allow administrators to create, edit, and manage various aspects of the CAVE application through a user-friendly interface.
    - `admin.py`: This file contains the configuration for the Django admin interface, including the registration of models and customization of the admin site for managing CAVE projects.
    - `apps.py`: This file contains the configuration for the CAVE application, including the definition of the application name and any necessary setup for the app to function properly within a Django project.
    - `auth.py`: This file contains the authentication logic for the CAVE application, including any custom authentication backends, user models, or authentication-related utilities that are necessary for managing user access and permissions within the CAVE projects.
    - `forms.py`: This file contains the forms used in the CAVE application for various purposes such as user input, data validation, and form handling. These forms are essential for creating interactive features and managing user interactions within the CAVE projects.
    - `middleware.py`: This file contains middleware classes that are used to process requests and responses in the CAVE application. Middleware can be used for various purposes such as authentication, logging, and modifying request/response data.
    - `models.py`: This file contains the database models for the CAVE application, defining the structure of the data that will be stored and managed within the CAVE projects. These models are essential for creating and managing the data layer of the application.
        - Model based logic is tied directly into the models.py file to ensure that the logic is easily accessible and maintainable. This includes any methods or functions that are directly related to the data models and their interactions within the CAVE application.
    - `resources.py`: This file contains the resource definitions for the CAVE application, which may include API resources, serializers, or other components that are necessary for managing the data and interactions within the CAVE projects.
    - `url_helpers.py`: This file contains helper functions for managing URLs within the CAVE application, such as getting extra content for view request. 
    - `views`: This folder contains a set of view files that handle the various views and endpoints for the CAVE application. These views are responsible for processing requests, interacting with the models, and returning appropriate responses to the users of the CAVE projects.
    - `websockets`: This folder contains the websocket logic for the CAVE application, which allows for real-time communication and updates between the server and clients in the CAVE projects. This is essential for features that require live updates or interactions within the app.
        - Websocket logic should match the cave_static API structure and enables the use of `cave_static` as a frontend framework for rendering each cave_app.
    - `utils`: This folder contains utility functions and helpers that handle things like `cache`, `constants`, `emailing`, `session_persistence`, `timing`, `validators` and `wrapping` logic.
    - `management`: This folder contains custom Django management commands such as `cache_test` and `clearcache`.
    - `migrations`: This folder contains Django database migrations for the cave_core models.
- /media: This directory is used for storing media files that are uploaded or generated by the CAVE application. It serves as the storage location for any user-generated content or media assets that are associated with the CAVE projects.
- /static: This directory is used for storing static files such as CSS, JavaScript, and images that are used in the frontend of the CAVE application. It serves as the location for all static assets that are needed to render the user interface of the CAVE projects.
- /templates: This directory contains the HTML templates that are used to render the views of the CAVE application. These templates define the structure and layout of the web pages that users interact with when using the CAVE projects.
- /utils: This directory contains cave cli utility functions that can be used to start the app, clear the database and more.

Testing:
- All tests are located in the `cave_api/tests` directory.
- In general, testing is not meant to be run after each edit, but may be depending on an api designer's preferences. The default tests are not meant to be acual tests. They are meant to be edited and added to as the API is developed.
- Containerized testing: `cave test -all`
    - To run a specific test file in Docker, you can run `cave test file_name.py`. 
    - This command will execute the specified test file within the Docker container, allowing you to test specific functionality or components of your CAVE project without running the entire test suite.

Linting:

- Linting is always done with `cave prettify` to ensure consistent formatting across all api code and tests.
- Linting everything can be done with `cave prettify -all` which will run the linter across the entire codebase to ensure that all code adheres to the defined style guidelines and formatting rules.

Other Instructions:

Ignore content in gitignored files like __pycache__, venv, .claude, *.egg-info, build, dist, etc. is not relevant to the codebase and should not be considered when making edits or suggestions.


