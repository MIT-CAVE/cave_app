#!/usr/bin/env python
import os

# Arguments
from cave_utils import Arguments
arguments = Arguments()

if __name__ == '__main__':
    # Set deployment type
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'cave_app.settings.{arguments.get_kwarg("deployment_type", "development")}')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Remove deployment_type from arguments
    arguments.delete('deployment_type', silent=True)
    # Start Django
    execute_from_command_line(arguments.get_arg_list())
