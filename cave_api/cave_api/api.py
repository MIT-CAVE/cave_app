# This is the entry point for the Cave API.
# It must define or import a function named `execute_command`.

# ── Option 1 (default): Browse all examples via the example selector ──────────
# The example selector lets you switch between all included examples from
# within the running app. It is useful for exploring what is possible, but
# is not intended as a coding template.
# To view the code for a specific example, open the corresponding file in:
#   cave_api/cave_api/examples/
from cave_api.cave_api.examples.selector.example_selector import execute_command

# ── Option 2: Start your own app ──────────────────────────────────────────────
# Uncomment the line below and comment out Option 1 above.
# cave_api/cave_api/src/app.py is a minimal starting template for your app.
# from cave_api.cave_api.src.app import execute_command

# ── Option 3: Load a specific example directly ────────────────────────────────
# Uncomment one of the lines below and comment out Option 1 above.
# from cave_api.cave_api.examples.api_command import execute_command
# from cave_api.cave_api.examples.map_nodes import execute_command
