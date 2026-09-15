#!/bin/sh
set -e

PORT="${PORT:-8081}"
exec /usr/bin/pgweb --bind=0.0.0.0 --listen="$PORT" --url="$DATABASE_URL"
