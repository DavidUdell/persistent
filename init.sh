#!/bin/bash

# Export secret, when present
if [ -f ./.secrets/secret_api_export.sh ]; then
    source ./.secrets/secret_api_export.sh
fi

docker pull ghcr.io/davidudell/persistent:latest
docker system prune -f

xhost +local:docker

# Trying to hook up X11 inside the container to outside
docker run -it \
    -e OPENAI_API_KEY=$OPENAI_API_KEY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    ghcr.io/davidudell/persistent:latest
