# Introduction

This documentation is intended for teams that are creating an API for use with the `CAVE App`.

This covers topics related to the python wrapper `cave_api` as part of `cave_app`.

**The detailed API documentation can be found [here](README_API_STRUCTURE.md)**

The `CAVE App` includes:

- [cave_app](https://github.com/MIT-CAVE/cave_app) - API Data Provider
- [cave_static](https://github.com/MIT-CAVE/cave_static) - API Data Consumer

## Designed for API Creators

The `CAVE App` is designed such that API Creators should be able to quickly tie advanced methods and models via API code into a productive user experience. The created experience should be easy to deploy to a website and have a wide variety of other web application features that API users can take advantage of without having to code.

API creators should not need to look at code from `cave_static`. As the CAVE team makes new `cave_static` releases, they provide these releases as a static build via a CDN at `https://builds.mitcave.com/major.minor.patch/index.html`. At the same time, the new `cave_app` version is released which includes updates to the example APIs and this documentation.

The `CAVE App` is also designed such that API creators should not have to write any server or hosting code (Django & React), however each project expects server code to be housed in the same project as the API code. In the event of distributed server production environments, this allows for distributed deployments with shared state handled by a load balancer.

## Versioning

Both `cave_app` and `cave_static` are versioned and kept in sync with releases. Each release is composed of a major version, a minor version and patch version (example `1.0.0`). Major versions are incremented when there is a breaking change in the API. Minor versions are incremented as we release new features that are not breaking changes within the API. Patch versions are updated as we push bug fixes.

This structure guarantees some nice features for API developers who want forward compatible upgrades from provider to consumer. As an example:

1. You start a project using `cave_app 1.0.0` using `cave_static 1.0.0`
2. A new chart type becomes available in `cave_static 1.2.0`
3. You update your environment in `cave_app 1.0.0` to now point to `cave_static 1.2.0`
    - You edit `globals.static_app_url_path` value in the admin page
        - Alternatively, you can run `cave reset` after updating your `.env`
    - Your app will continue to work as it worked on `cave_static 1.0.0` with the new chart available
        - Remember: breaking API changes only occur between major version changes
        - Since you stayed on `1.x.y` you get a free forward compatible upgrade

- Note: If you start developing on `cave_app 1.x.y`, it will only work with `cave_static 1.a.b` where the `a>x` or `a=x & b>y`

# Making changes

To make changes to the `cave_api`, navigate to `<your_app>/cave_api/cave_api` and begin to make adjustments.

By default the `cave_api` uses the `static_model` listed in `<your_app>/cave_api/cave_api`. To change this over to the `serialization_model`:
- Edit `<your_app>/cave_api/cave_api/__init__.py`
- Replace `static_model` with `serialization_model`
- Save the file

Using the `static_model` is a great way to explore the functions available in the `cave_api`. It does not do anything, but it is helpful to explore how the API can control the UI.

As an example of how to do this, lets add a flag button to the static model that calls the api and has it print `Hello World!`.
- NOTE: Make sure you switched the app back over to `static_model` using the instructions above before starting this step.

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
4. Click on the sessions icon (top left of the page - furthest icon to the right)
    - Create a new session named `s1`
    - You should now be looking at the app for `static_model`
5. Now edit the `static_model`:
    - Edit `<your_app>/cave_api/cave_api/static_model/api.py`
        - In this file, there is one large `example` variable (a python dictionary) that creates all the needed API values in one place.
        - In the `example` dictionary edit `appBar.data` to add the following key:
            ```
            "myButton":{
                "name": "My Button",
                "icon": "MdFlag",
                "apiCommand": "myCommand",
                "type": "button",
                "bar": "upper",
                "order":7,
            }
            ```
        - Near the end of the file after:
            ```
            if command == 'reset':
                  return example
            ```
            Add the following code:
            ```
            if command == 'myCommand':
                print ("Hello World!")
            ```
6. Going back to Chrome, click the refresh button just above the lightning bolt on the app bar (left hand side of the page) to update your data.
    - You should now see your new button (the flag).
    - Click on your button to see the output `Hello World!` printed in your terminal.

## Adding Requirements to the API

Python requirements can be added to the API by adding line items to `your_app/cave_api/requirements.txt`.
- **NOTE**: These requirements should not be added in the `your_app/requirements.txt` or `utils/extra_requirements.txt` files as these are designed for server use.

Once added, you can update your python environment by running (in the root of your app):
```
cave reinstall-pkgs
```

## Adding Static Data to the API

To add static data to the api:
- Make sure it is located in: `your_app/cave_api/cave_api`
- Depending on how the `cave_api` package is installed, the location of this file may fundamentally change.
    - To access this file, use something similar to the following inside of your code to get the relative data path:
    ```
    import pkg_resources
    data_location = pkg_resources.resource_filename('cave_api', 'simple_model/data/')
    ```

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


# Appendix

## Changing the API Code
To fundamentally change the API structure, API developers can always fork a specific version of `cave_static`, make any adjustments, and host a build at their desired location. Then they can update their version of `cave_app` to match these changes.
