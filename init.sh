#! /bin/bash

# Docker image and container management
docker pull ghcr.io/davidudell/persistent:latest
docker system prune -f
docker run -it ghcr.io/davidudell/persistent:latest
