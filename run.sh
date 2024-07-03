#!/bin/bash

# Set environment or development by default
ENVIRONMENT=${1:-development}

# Export the environment variable
export ENVIRONMENT

# Run the alembic command
alembic upgrade head

# Run the uvicorn server
uvicorn main:app --reload
