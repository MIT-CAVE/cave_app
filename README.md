# Cave App
A Django server to host the an API and act as the Cave back end.

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
