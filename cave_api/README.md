# Introduction

This documentation is intended for teams that are creating their own custom `CAVE App`.

Specifically, this covers topics related to the `cave_api` as part of `cave_app`.

**The detailed API documentation can be found [here](https://mit-cave.github.io/cave_utils/cave_utils/api.html)**

**Detailed API examples can be found [here](https://github.com/MIT-CAVE/cave_app/tree/main/cave_api/cave_api/examples)**

# What is a `CAVE App`?

## Designed for Customization and Deployment

The `CAVE App` is designed such that custom CAVE App creators (app creators) should be able to quickly integrate advanced methods and models from Python into a productive user experience via a simple API. The created experience should be easy to deploy to a website. It should also have a wide variety of other web application features that app creators can take advantage of with little or no additional code.

The `CAVE App` is also designed such that app creators should not have to write any back end or front end code (Django & React). With that said, each project expects back end (Django) code to be housed in the same project as the API code. This allows for local development and production web deployments including horizontally and vertically scalable systems. In the event of distributed server production environments, this allows for distributed deployments with shared state handled by a load balancer.

## Related Projects

There are related supporting projects for each custom `CAVE App` (we will call this `your_app`). These include `cave_utils`, `cave_static` and `cave_cli`.

The `cave_utils` project is python package. It comes with some helpful python utility functions that are used throughout `your_app`. These include helpful logging features, api validation features, and more. The `cave_utils` project is also used to generate the detailed [API spec documentation](https://mit-cave.github.io/cave_utils/cave_utils/api.html). Static builds of `cave_utils` are available from [pypi](https://pypi.org/project/cave-utils). This package is automatically installed when running `your_app` using the `cave_cli`. It is listed in `your_app/requirements.txt`.

The `cave_static` project represents a static build of the front end code (React). Each browser that accesses `your_app` will load one of these static builds and use it to render the app page of your `cave_app`. It essentially consumes the API to create the actual user experience. The `cave_static` project is hosted on a CDN. The exact build `your_app` uses is determined by the location set in your `your_app/.env`

The `cave_cli` project offers an easy to use command line interface to interact with `your_app`. This includes creating an app, starting the app, running tests, and more. You can see the full list of commands by running `cave help`. You can find the `cave_cli` project [here](https://github.com/MIT-CAVE/cave_cli).

## Versioning

The core `cave_app` projet and supporting projects are versioned and offered in sychronized releases. Each release is composed of a major version, a minor version and patch version (example `1.0.0`). Major versions are incremented when there is a breaking change in the API. Minor versions are incremented as we release new features that are not breaking changes within the API. Patch versions are updated as we push bug fixes.

This structure guarantees some nice features for API developers who want forward compatible upgrades. As an example:

1. You start a project using `cave_app 2.0.0` using `cave_static 2.0.0`
2. A new chart type becomes available in `cave_static 2.2.0`
3. You choose to update `your_app` running `cave_app 2.0.0` to now point to `cave_static 2.2.0`
    - You go to your admin page and edit `globals.static_app_url_path` value in the admin page
        - Alternatively, you can run `cave reset-db` after updating your `your_app/.env`
    - Your app will continue to work as it worked on `cave_static 2.0.0` with the new chart available
        - Remember: breaking API changes only occur between major version changes
        - Since you stayed on `2.x.y` you get a free forward compatible upgrade with no updates needed for your api or server code.

- Note: If you start developing on `cave_app 2.x.y`, it is only guaranteed to work with `cave_static 2.a.b` where the `a>x` or `a=x & b>y`

App creators will have access to new `cave_static` versions as they they become stable releases. You can see the list of `cave_static` versions by checking our [cave_static branches on github](https://github.com/MIT-CAVE/cave_static/branches/all). Stable branches are branches that do not include `-dev` in their name. When it is time for a version to become stable, we remove the `-dev` tag from the branch and upload the accompaning build. These releases are accessable via our CDN at `https://builds.mitcave.com/major.minor.patch/index.html`. At the same time, the new `cave_app` version is released which includes updates to any example APIs and this documentation. 

New versions of `cave_utils` will be released as needed. These will be available on [pypi](https://pypi.org/project/cave-utils). In your `your_app/requirements.txt` file, this package is listed as `cave-utils>=x.y.z` where `x.y.z` is the version you are using. Because Docker may cache your individual package versions, you may need to update your `your_app/requirements.txt` file to get the latest version of `cave_utils`. To do this, simply update the version number to the latest version available on [pypi](https://pypi.org/project/cave-utils). As an example, if you are using `cave_utils 2.0.0` and `cave_utils 2.0.1` is released, you may need to update your `your_app/requirements.txt` file to `cave-utils>=2.0.1`. This will ensure you are using the latest major version of `cave_utils` available on [pypi](https://pypi.org/project/cave-utils).


Special Note: Patch version releases may not align between projects, but major and minor versions will always align. As an example, `cave_app 2.0.0` will always be released with `cave_static 2.0.0` and `cave_utils 2.0.0`. However, `cave_app 2.0.1` may be released with `cave_static 2.0.1` and `cave_utils 2.0.2`. This is because `cave_utils` may have a bug fix that is not needed in `cave_static` or `cave_app`.

# Making changes

To make changes to the `cave_api`, navigate to `your_app/cave_api/cave_api` and begin to make adjustments.

The main entrypoint to the `cave_api` is in `your_app/cave_api/cave_api/api.py`. This file must have a function `execute_command` that serves as the primary entrypoint for all incoming requests. This function is responsible for parsing the incoming request and handling it accordingly. This function is also responsible for returning the appropriate response to the request.

By default the `your_app/cave_api/cave_api/api.py` imports `execute_command` from `your_app/cave_api/cave_api/example_selector.py`. This is a meta model that allows you to choose from any of the api models listed in `your_app/cave_api/cave_api/examples`. You can modify any of the examples while using the default example selector and see your changes live by choosing the example in the app menu.

To change over to any specific example or your own code, you can edit `your_app/cave_api/cave_api/api.py` accordingly. Replace the import location for `execute_command` or simply define `execute_command` in this file and save. You may need to reset your database to see these changes take effect. To do this, run `cave reset` from your project root.

## Changing an Example

As an example of how to edit the api, lets add a flag button to the `api_command.py` example that calls the api and has it print `Hello World!`.
- NOTE: Make sure `your_app/cave_api/cave_api/api.py` is importing from `cave_api.examples.example_selector`. 

1. Start the app:
    ```
    cd path/to/your_app
    cave run
    ```
2. Open `http://localhost:8000` in Google Chrome.
3. Log in using the login icon in the top right corner of the app.
    - For now, you can log in with:
        - Username: `admin`
        - Password: The password you set when creating the app (stored in `your_app/.env`)
4. Click on the app page:
    - You should now be looking at the app for your currently selected example.
5. Now edit `your_app/cave_api/cave_api/examples/api_command.py`:
    - In the block `if command == "init"` add the following key to `appBar.data`:
        ```
        "sayHelloButton": {
            "icon": "md/MdFlag",
            "apiCommand": "sayHello",
            "type": "button",
            "bar": "lowerLeft",
        },
        ```
    - Near the end of the file after the `elif command == "myCommand"` block and before raising an exception, add the following code:
        ```
        elif command == "sayHello":
            # Send a message to the user
            socket.notify("Hello World!")
            # Print a message to the terminal
            print("Hello World!")
            return session_data
        ```
6. Going back to Chrome, in the top left corner click on the 3 sliders icon and choose the `api_command.py` example. If you are on the current exmaple, you might need to click on the refresh button just below the 3 sliders. 
    - You should now see your new button (the flag) in the bottom left corner.
    - Click on your button to see the output `Hello World!` sent to the chrome page as a notification and printed in your terminal.

## Adding Requirements to the API

Python requirements can be added to the API by adding line items to `your_app/cave_api/requirements.txt`.
- **NOTE**: These requirements should **not** be added in the `your_app/requirements.txt` or `your_app/utils/extra_requirements.txt` files as these are designated for server use.

Once added in this requirements file, your docker environment will be updated the next time you start it (cave run, cave test ...). It is possible that you may experience issues after adding these requirements. To debug this, try running your app in verbose mode `cave run -v` to see if there are any errors.

You may have to kill your current running app to get this change. To do this, use `Ctrl + C` in the terminal running your app.

You can update your python environment by running your app again (EG: in verbose mode for debugging):
```
cave run -v
```

<br/>
<details>
  <summary>Unable to import a package? Click Here</summary>
<br/>
If you notice issues or cannot install/import packages specified in `your_app/cave_api/requirements.txt`, consider running the app in interactive mode:
```
cave run -it
```

Then in your container terminal, run:
```
pip install -r cave_api/requirements.txt
```

You should see some errors as to why the package is not installing. 
    - This is usually due to a missing dependency. 
    - You may need to install a system level package.

To Fix this, update your dockerfile to `RUN` the needed steps to resolve the dependency issue.

Example:

- As an example, you add `rasterio==1.3.7` to `your_app/cave_api/requirements.txt`
    - When you start your app again, you notice that it fails to start or you can not complete a function because `rasterio` is missing.
- Run `cave run -it` and try to install the requirements manually:
    ```
    pip install -r cave_api/requirements.txt
    ```
- You may see an error like:
    ```
    Error: A GDAL API version must be specified. Provide a path to gdal-config using a GDAL_CONFIG environment variable or use a GDAL_VERSION environment variable.
    ```
- A quick google search will show that you need to install `gdal-bin` and `libgdal-dev` system packages to resolve this issue.
- To install this in your container image (EG: python:3.11.3-bullseye - which runs on debian), you might find that you need to run:
    ```
    apt-get update && apt-get install -y gdal-bin libgdal-dev
    ```
- If you can then successfully run `pip install -r cave_api/requirements` in the interactive terminal, you have solved your problem.
- You can exit your interactive terminal by typing `exit` and hit enter.
- This process now needs to be added to you Dockerfile.
    - To do this, edit `your_app/Dockerfile` and add the following lines before the `RUN pip install -r cave_api/requirements.txt` line:
    ```
    RUN apt-get update
    RUN apt-get install -y gdal-bin libgdal-dev
    ```
- Now, when you run your app, the DOCKER image will be built again and `rasterio` should install correctly 
    - The app should work assuming you have no other issues.
</details>
<br/>

## Adding Static Data to the API

To add static data to the api:
- Make sure it is located in: `your_app/cave_api/cave_api`
- Depending on how the `cave_api` package is installed, the location of this file may fundamentally change.
- To access a static file, use something similar to the following inside of your code.
    - This gets the relative data path to the current pip package location:
    ```
    import json
    from importlib import resources
    data_location = resources.files("cave_api.data")
    relative_data_path = data_location.joinpath("api.json").__str__()
    ```
- See: [static data example](/cave_api/cave_api/examples/static_data_example.py) for a simple example.
- Note: It is important to use `importlib.resources` to access files in the package.
    - The actual location of the data folder might change depending on how the package is installed.
    - This is particularly important when deploying the package (EG: AWS using Elastic Beanstalk).
    - Often, the package location at installation is different from production for rolling deployment processes.

## Testing

You can create test scripts that allow you to validate your API functionality.
- These should be located in `your_app/cave_api/tests/`
- An example test is found in `your_app/cave_api/tests/test_init.py`
- To run tests (while in your project root):
```
cave test <your-test>
```
- Example:
```
cave test test_init.py
```

## Debugging

### API Data Validation:

- You can use live automated API validation by updating `LIVE_API_VALIDATION_PRINT` or `LIVE_API_VALIDATION_LOG` in your `your_app/.env` file.
- An alternative to this is to use the `cave test` command to run your tests.
    - Include any validation tests in your test scripts
- You can also manually validate your api code with the `cave_utils` package
    - See the [cave_utils documentation](https://github.com/mit-cave/cave_utils) for more information

### Testing: 

- A great way to debug is through the `cave test` command in your terminal. 
    - Use `cave help` for more information on that function.
- You can add print statements to your code as you work through that process and `cave test` would yield those in your terminal
- Pairing this with the `cave_utils` package can be a great way to test/debug your code

### Console:

- Assuming your API Data Validation passes without any issues, but something is still crashing (when the app goes grey and only the app bar is left), the console is a great next step to debug the situation
- Launch your app using `cave run`
- Log in to the app and go to the `app` page.
- Inspect chrome
    - On Mac: Cmd + Option + i
    - On Linux: Ctrl + Shift + i
- Navigate to the console tab and note any log items that may help you to debug your issue.
