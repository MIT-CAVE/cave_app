# Introduction
This documentation is intended for teams that are creating an API for use with the `CAVE App`.

This covers topics related to the python wrapper `cave_api` as part of `cave_app`.

**The detailed API documentation can be found [here](README_API_STRUCTURE.md)**

The `CAVE App` includes:

- [cave_app](https://github.com/MIT-CAVE/cave_app) - API Data Provider
- [cave_static](https://github.com/MIT-CAVE/cave_static) - API Data Consumer

## Designed for API Creators
The `CAVE App` is designed such that API Creators should be able to quickly tie advanced methods and models via API code into a productive user experience. The created experience should be easy to deploy to a website and have a wide variety of other web application features that API users can take advantage of without having to code.

API creators should not need to look at code from `cave_static`. As the CAVE team makes new `cave_static` releases, they provide these releases as a static build via a CDN at `https://builds.mitcave.com/major.minor.patch/index.html`. At the same time, the new `cave_server` version is released which includes updates to the example APIs and this documentation.

The `CAVE App` is also designed such that API creators should not have to write any server or hosting code (Django & React), however each project expects server code to be housed in the same project as the API code. In the event of distributed server production environments, this allows for distributed deployments with shared state handled by a load balancer.

## Versioning
Both `cave_server` and `cave_static` are versioned and kept in sync with releases. Each release is composed of a major version, a minor version and patch version (example `1.0.0`). Major versions are incremented when there is a breaking change in the API. Minor versions are incremented as we release new features that are not breaking changes within the API. Patch versions are updated as we push bug fixes.

This structure guarantees some nice features for API developers who want forward compatible upgrades from provider to consumer. As an example:

1. You start a project using `cave_server 1.0.0` using `cave_static 1.0.0`
2. A new chart type becomes available in `cave_static 1.2.0`
3. You update your environment in `cave_server 1.0.0` to now point to `cave_static 1.2.0`
  - You edit `globals.static_app_url_path` value in the admin page
    - Alternatively, you can run `./utils/reset_db.sh` after updating your `.env`
  - Your app will continue to work if it worked on `cave_static 1.0.0`
    - Breaking API changes only occur between major version changes
    - Since you stayed on `1.x.y` you get a free forward compatible upgrade

- Note: If you start developing on `cave_server 1.x.y`, it will only work with `cave_static 1.a.b` where the `a>x` or `a=x & b>y`

# Local Testing Setup
Make sure you have Python 3.9.x (or higher) installed on your system
- You can download it [here](https://www.python.org/downloads/)

Set up pip installation requirements
- Pip installation requirements need to be specified in `setup.py`. See more [here](https://packaging.python.org/discussions/install-requires-vs-requirements/)

## Installation
To egg install (hot load changes):
```
pip install -e path/to/cave_api
```

## Adding Requirements to the API
Python requirements can be added to the API by adding line items in `install_requires` in `cave_api/setup.py`.

NOTE: They should not be added in the `requirements.txt` or `utils/extra_requirements.txt` files as these are designed for server use.

## Testing
Example: Create a simple testing script that configures an initial session:
- Note: The process below is done automatically by the server during session creation.
```py
from cave_api import execute_command
initial_session_data=execute_command(session_data={}, command='init')
print(initial_session_data)
```

# Appendix

## Changing the API Code
To fundamentally change the API structure, API developers can always fork a specific version of `cave_static`, make any adjustments, and host a build at their desired location. Then they can update their version of `cave_server` to match these changes.
