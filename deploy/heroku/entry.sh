#!/bin/bash

set -eu

echo "changin nginx PORT to $PORT"
sed -i 's/PORT/'"$PORT"'/g' /recipebook/nginx.conf
# export RECIPEBOOK_PUBLIC_URL=${RECIPEBOOK_PUBLIC_URL:-https://$HEROKU_APP_NAME.herokuapp.com}
