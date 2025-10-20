#!/bin/bash

# Simple rsync deployment script
# Usage: ./deploy/sync.sh [server]

SERVER="${1}"
REMOTE_PATH="${REMOTE_PATH:-//srv/site/}"

if [ -z "$SERVER" ]; then
  echo "Error: You must provide a server as the first argument."
  exit 1
fi

echo "Deploying to $SERVER..."

rsync -avz --delete \
  --include='tssite/' \
  --include='tsAdmin/' \
  --include='manage.py' \
  --include='pyproject.toml' \
  --include='uv.lock' \
  --exclude='*/__pycache__/' \
  --exclude='*' \
  ./ "$SERVER:$REMOTE_PATH/"

echo "Deployment complete!"

echo "Restarting service..."

ssh "$SERVER" "sudo systemctl restart gunicorn-tsadmin"

echo "Service restarted!"