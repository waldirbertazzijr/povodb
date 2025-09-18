#!/bin/bash
# direct-init.sh - Direct database initialization for PovoDB

set -e

echo "=== PovoDB Direct Database Initialization ==="
echo "Waiting for PostgreSQL to be ready..."

# Wait for PostgreSQL to be ready
pg_isready -h db -p 5432 -U postgres -t 60

# Run the initialization SQL script
echo "Initializing database with direct SQL..."
PGPASSWORD=postgres psql -h db -U postgres -d povodb -f /app/direct-init-db.sql

echo "Database initialization complete!"
echo "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
