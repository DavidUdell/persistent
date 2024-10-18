#!/bin/bash
set -e

export DISPLAY=:99

Xvfb :99 -screen 0 1024x768x16 &

api_key=$OPENAI_API_KEY
len_api_key=${#api_key}

# Ensure the key is not empty.
if [ $len_api_key -gt 1 ]; then
    python3 src/browser_loop.py
fi

exec "$@"
