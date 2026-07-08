#!/bin/sh
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Running seed data..."
python -m seeds.seed

echo "Starting uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
