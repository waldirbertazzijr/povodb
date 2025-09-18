#!/usr/bin/env python
"""
Alembic initialization script for PovoDB.

This script creates the initial Alembic revision based on the SQLAlchemy models.
Run this once to initialize the database schema for PovoDB.
"""

import os
import sys
import subprocess
from pathlib import Path

# Ensure we're in the correct directory
script_dir = Path(__file__).parent.absolute()
os.chdir(script_dir)

# Print banner
print("=" * 80)
print("PovoDB Alembic Initialization")
print("=" * 80)

# Check if alembic directory exists
if not Path("alembic").exists():
    print("Error: alembic directory not found. Make sure you're in the right directory.")
    sys.exit(1)

try:
    # Initialize Alembic if not already initialized
    if not Path("alembic/versions").exists():
        print("Creating 'alembic/versions' directory...")
        Path("alembic/versions").mkdir(exist_ok=True)

    # Check if there are any existing revisions
    existing_revisions = list(Path("alembic/versions").glob("*.py"))
    if existing_revisions:
        print(f"Found {len(existing_revisions)} existing revisions.")
        print("Proceeding with database upgrade...")
    else:
        # Create initial migration
        print("Creating initial migration...")
        subprocess.run(["alembic", "revision", "--autogenerate", "-m", "Initial migration"], check=True)
        print("Initial migration created successfully!")

    # Run upgrade
    print("Applying migrations...")
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    print("Database schema created/updated successfully!")

except subprocess.CalledProcessError as e:
    print(f"Error during migration process: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)

print("=" * 80)
print("PovoDB database initialization complete!")
print("=" * 80)
