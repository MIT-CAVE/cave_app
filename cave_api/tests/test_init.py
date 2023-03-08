from cave_api import execute_command


class Socket:
    def __init__(self):
        pass

    def broadcast(self, *args, **kwargs):
        print("broadcast: ", {"args": args, "kwargs": kwargs})

    def notify(self, *args, **kwargs):
        print("notify: ", {"args": args, "kwargs": kwargs})

init_session_data = execute_command(session_data={}, socket=Socket(), command="init")

init_keys = init_session_data.keys()

for check_key in [
    "appBar",
    "arcs",
    "categories",
    "dashboards",
    "geos",
    "kpis",
    "kwargs",
    "maps",
    "nodes",
    "panes",
    "settings",
    "stats",
]:
    if check_key not in init_keys:
        raise Exception(
            f"Missing `{check_key}` top level key given empty session data and `init` command."
        )

print("test_init.py passed!")
