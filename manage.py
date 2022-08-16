#!/usr/bin/env python
import os
import sys

def get_value(key, arg_dict, default, acceptable_values=None):
    out_val=arg_dict.get(key, default)
    if isinstance(acceptable_values, list):
        if out_val not in acceptable_values:
            print(f'{key} = {out_val}, but acceptable values only include {str(acceptable_values)}.\nDefaulting to {default}')
            out_val = default
    return out_val

def remove_specific_args(keys, args):
    arg_idxs = [idx for idx, arg in enumerate(args) if arg in keys]
    return [arg for idx, arg in enumerate(args) if (idx not in arg_idxs and idx-1 not in arg_idxs)]

if __name__ == '__main__':
    # Validate .env exists
    if not os.path.isfile('.env'):
        raise Exception ("Error: No .env file found. Create the '.env' file by following the setup instructions in the readme.md.")

    # Argument Dictionary
    argument_keys = ["--deployment_type"]
    arg_dict = y={i:sys.argv[idx+1] for idx, i in enumerate(sys.argv) if i in argument_keys}
    args = remove_specific_args(argument_keys, sys.argv)

    # Argument Values
    deployment_type = get_value('--deployment_type', arg_dict, 'development')
    # Set deployment type
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'cave_app.settings.{deployment_type}')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(args)
