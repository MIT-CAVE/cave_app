from cave_api import execute_command

initial_session_data=execute_command(session_data={}, command='init')

print(initial_session_data.get('settings',{}).get('data'))
