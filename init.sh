#!/bin/bash

# Export secret, when present
if [ -f ./.secrets/secret_api_export.sh ]; then
    source ./.secrets/secret_api_export.sh
fi

# Docker image and container management
docker pull ghcr.io/davidudell/persistent:latest
docker system prune -f
docker run -it -e OPENAI_API_KEY=$OPENAI_API_KEY ghcr.io/davidudell/persistent:latest
