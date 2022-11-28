
check_envs() {
  if ! [[ -f "./.env" ]]; then
    printf "Error: No .env file found. Create the '.env' file by following the setup instructions in the readme.md.\n"
    exit 1
  fi
}

check_migrations() {
  if ! [[ -f "./cave_core/migrations/0001_initial.py" ]]; then
    printf "\n\nWarning: No initial migration found for app. One was created for you by running:\n\n'python3 manage.py makemigrations cave_core'\n\n"
    python3 manage.py makemigrations cave_core
  fi
}

nuke_linux_db() {
  source .env
  sudo -u postgres psql -c "DROP DATABASE IF EXISTS $DATABASE_NAME"
  sudo -u postgres psql -c "DROP USER IF EXISTS $DATABASE_USER"
  sudo -u postgres psql -c "CREATE DATABASE $DATABASE_NAME"
  sudo -u postgres psql -c "CREATE USER $DATABASE_USER WITH ENCRYPTED PASSWORD '$DATABASE_PASSWORD'"
  sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DATABASE_NAME TO $DATABASE_USER"
}

nuke_mac_db() {
  source .env
  psql postgres -c "DROP DATABASE IF EXISTS $DATABASE_NAME"
  psql postgres -c "DROP USER IF EXISTS $DATABASE_USER"
  psql postgres -c "CREATE DATABASE $DATABASE_NAME"
  psql postgres -c "CREATE USER $DATABASE_USER WITH ENCRYPTED PASSWORD '$DATABASE_PASSWORD'"
  psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DATABASE_NAME TO $DATABASE_USER"
}

nuke_db() { # Check the OS and nuke the db using the relevant process.
  case "$(uname -s)" in
      Linux*)     machine="Linux";;
      Darwin*)    machine="Mac";;
      *)          machine="UNKNOWN"
  esac
  if [ $machine = "UNKNOWN" ]; then
    printf "Error: Unknown operating system.\n"
    printf "Please run this command on one of the following:\n"
    printf "- MacOS\n- Linux\n- Windows (Using Ubuntu 20.04 on Windows Subsystem for Linux 2 - WSL2)"
    exit 1
  elif [ $machine = "Linux" ]; then
    printf "\nLinux recognized. Attempting to Nuke your db (sudo required)...\n"
    nuke_linux_db
  elif [ $machine = "Mac" ]; then
    printf "\nMac recognized. Attempting to Nuke your db (sudo required)...\n"
    nuke_mac_db
  else
    printf "Error: Reset DB failed.\n"
    exit 1
  fi
  printf "Nuke complete\n\n"
}

clear_pycache() {
  printf "Cleaning Pycache (sudo required)...\n"
  sudo rm -r "./cave_core/__pycache__"
  sudo rm -r "./cave_core/migrations/__pycache__"
  sudo rm -r "./cave_app/settings/__pycache__"
  sudo rm -r "./cave_app/__pycache__"
  printf "Pycache Cleaning Complete!\n\n"
}

make_tmp() {
  mkdir "./tmp"
}

del_tmp() {
  sudo rm -r "./tmp"
}

get_migrations() {
  printf "$(ls ./cave_core/migrations/*.py)" > "./tmp/$1.txt"
}

make_django_migrations() {
  # Ensure initial migration files are present
  check_migrations
  # Generate any temp migrations that might need to be applied on the fly
  printf "Generating and Applying New Migrations...\n"
  # Create a temporary directory
  make_tmp
  # Store initial migrations in the temporary directory
  get_migrations "initial_migrations"
  # Make the migrations
  python3 manage.py makemigrations cave_core --deployment_type development
  # Apply the migrations
  python3 manage.py migrate --deployment_type development
  # Create the cache table
  python3 manage.py createcachetable
  # Store all new migrations in the temporary directory
  get_migrations "all_migrations"
  # Determine new migrations that have been applied
  grep -Fxvf ./tmp/initial_migrations.txt ./tmp/all_migrations.txt > ./tmp/new_migrations.txt
  # Remove auto generated migrations for deployment and git clenliniess
  cat ./tmp/new_migrations.txt | while read migration_name; do
    sudo rm $migration_name
  done
  del_tmp
  printf "Migration Process Complete!\n\n"
}

generate_data() {
  printf "Generating Data...\n"
  python3 data_gen.py --deployment_type development
  printf "Data Generation Complete!\n"
}

main() {
  # Change to the script directory
  cd "$(dirname "$0")/.."
  # Ensure the environment files are present
  check_envs
  # Clear out the existing db
  nuke_db
  # Clear out pycache
  clear_pycache
  # Make python migrations
  make_django_migrations
  # Generate Data
  generate_data
}

main "$@"
