#!/bin/bash
# wait-for-db.sh

set -e

HOST="$1"
PORT="$2"
TIMEOUT="${3:-30}"
INTERVAL="${4:-1}"

echo "Waiting for PostgreSQL on ${HOST}:${PORT}..."

elapsed=0
while [ "$elapsed" -lt "$TIMEOUT" ]; do
  if pg_isready -h "$HOST" -p "$PORT" -U postgres > /dev/null 2>&1; then
    echo "PostgreSQL is ready!"
    exit 0
  fi

  echo "PostgreSQL is not available yet. Waiting..."
  sleep "$INTERVAL"
  elapsed=$((elapsed + INTERVAL))
done

echo "Timed out waiting for PostgreSQL on ${HOST}:${PORT}"
exit 1
