#!/bin/bash
# Bash strict mode: http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

# Used by docker-entrypoint.sh to start the dev server
# If not configured you'll receive this: CommandError: "0.0.0.0:" is not a valid port number or address:port pair.
PORT="${PORT:-8000}"
DATABASE_USER="${DATABASE_USER:-postgres}"
DATABASE_HOST="${DATABASE_HOST:-db}"
DATABASE_PORT="${DATABASE_PORT:-5432}"

# Ensure the installed python dependencies are on the path and available.
export PATH="$PATH:$HOME/.local/bin"

postgres_ready() {
python << END
import sys
import psycopg2
try:
    psycopg2.connect(
        dbname="${DATABASE_NAME}",
        user="${DATABASE_USER}",
        password="${DATABASE_PASSWORD}",
        host="${DATABASE_HOST}",
        port="${DATABASE_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

wait_for_postgres() {
until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'
}



show_help() {
# If you change this please update ./docs/reference/recipebook-docker-api.md
    echo """
Usage: docker run <imagename> COMMAND
Commands
local     : Start django using a prod ready gunicorn server
dev       : Start a normal Django development server
bash      : Start a bash shell
manage    : Start manage.py
python    : Run a python command
shell     : Start a Django Python shell
celery    : Run celery
celery-dev: Run a hot-reloading dev version of celery
lint:     : Run the linting
help      : Show this message
"""
}

run_setup_commands_if_configured(){
if [ "$MIGRATE_ON_STARTUP" = "true" ] ; then
  echo "python /recipebook/backend/src/recipebook/manage.py migrate"
  python /recipebook/backend/src/recipebook/manage.py migrate
fi
# if [ "$SYNC_TEMPLATES_ON_STARTUP" = "true" ] ; then
#   echo "python /recipebook/backend/src/recipebook/manage.py sync_templates"
#   python /recipebook/backend/src/recipebook/manage.py sync_templates
# fi
}

case "$1" in
    dev)
        wait_for_postgres
        run_setup_commands_if_configured
        echo "Running Development Server on 0.0.0.0:${PORT}"
        echo "Press CTRL-p CTRL-q to close this session without stopping the container."
        CMD="python /recipebook/backend/src/recipebook/manage.py runserver 0.0.0.0:${PORT}"
        echo "$CMD"
        # The below command lets devs attach to this container, press ctrl-c and only
        # the server will stop. Additionally they will be able to use bash history to
        # re-run the containers run server command after they have done what they want.
        exec bash --init-file <(echo "history -s $CMD; $CMD")
    ;;
    local)
        wait_for_postgres
        run_setup_commands_if_configured
        exec gunicorn --workers=3 -b 0.0.0.0:"${PORT}" -k uvicorn.workers.UvicornWorker recipebook.config.asgi:application
    ;;
    bash)
        exec /bin/bash "${@:2}"
    ;;
    manage)
        exec python /recipebook/backend/src/recipebook/manage.py "${@:2}"
    ;;
    python)
        exec python "${@:2}"
    ;;
    shell)
        exec python /recipebook/backend/src/recipebook/manage.py shell
    ;;
    lint)
        CMD="make lint-python"
        echo "$CMD"
        exec bash --init-file <(echo "history -s $CMD; $CMD")
    ;;
    *)
        show_help
        exit 1
    ;;
esac