# Offer to reset the db if it has not yet been setup
if [ "$(python ./manage.py showmigrations --deployment_type development | grep "\[X\]" | wc -l)" -eq "0" ]; then
  printf "Your database has not been setup or is not properly configured." 2>&1 | pipe_log "WARN"
  # Ask the user if they want to reset the db
  printf "Would you like to reset the database using './utils/reset_db.sh'? (y/n): " 2>&1 | pipe_log "WARN"
  read -r reset_db
  if [ "$reset_db" = "y" ]; then
    printf "Resetting the database...\n" 2>&1 | pipe_log "WARN"
    source ./utils/reset_db.sh
    # Check if the db was reset successfully
    if [ "$(python ./manage.py showmigrations --deployment_type development | grep "\[X\]" | wc -l)" -eq "0" ]; then
      printf "Unable to reset the database.\n" 2>&1 | pipe_log "ERROR"
      exit 1
    fi
  else
    printf "Unable to start the app. Ensure your database is properly configured.\n" 2>&1 | pipe_log "ERROR"
    exit 1
  fi
fi