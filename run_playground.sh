#!/bin/bash

# Exit immediately if any command fails
set -e

echo "Building & starting pyzmq-playground container..."

# Build and bring up the container in one go
docker-compose up --build


# To run detached, uncomment this instead:
# docker-compose up -d

# Note:
# - Use Ctrl+C to stop if you ran in foreground.
# - Or: docker-compose down to stop if you ran in detached mode.
