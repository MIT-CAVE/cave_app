if ! command -v pipe_log &> /dev/null; then
  log() {
      local log_message=$1
      local log_priority=$2
      printf "$log_priority: $log_message\n" >&2
  }

  pipe_log() {
    IFS=''
    while read -r line || [ -n "$line" ]; do
      log "$line" "$1"
    done
  }
fi