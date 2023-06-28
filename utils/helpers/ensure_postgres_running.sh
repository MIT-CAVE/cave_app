# Poll Postgres Server
for i in {1..6}; do
  if [ ! $i -eq 6 ]; then
    if (source /app/.env && python3 -c "import psycopg2; psycopg2.connect(\"dbname='$DATABASE_NAME' user='$DATABASE_USER' host='$DATABASE_HOST' password='$DATABASE_PASSWORD'\")" 2>/dev/null); then
      break
    fi
  else
    printf "Postgres never came up...\nMaking one last attempt and logging any errors that occur:\n" 2>&1 | pipe_log "WARN"
    if (source /app/.env && python3 -c "import psycopg2; psycopg2.connect(\"dbname='$DATABASE_NAME' user='$DATABASE_USER' host='$DATABASE_HOST' password='$DATABASE_PASSWORD'\")"); then
      break
    else
      printf "Postgres never came up, exiting...\n" 2>&1 | pipe_log "ERROR"
      exit 1
    fi
  fi
  printf "Waiting for postgres ($i)...\n" 2>&1 | pipe_log "DEBUG"
  sleep 3
done