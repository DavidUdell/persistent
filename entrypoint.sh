#!/bin/bash
set -e

# In-container X11 setup.
# export DISPLAY=:99
# Xvfb :99 -screen 0 1024x768x16 &

api_key=$OPENAI_API_KEY
len_api_key=${#api_key}

apt install x11-apps -y

# Ensure the key is not empty.
if [ $len_api_key -gt 1 ]; then
    xclock
    python3 src/browser_loop.py
fi

exec "$@"
