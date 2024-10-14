# persistent
[![License:
MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A proof-of-concept persistent AI agent implementation

## Contents
The `/src` directory contains source code for the AI agent implementation.

## User's Guide
```
docker run -it ghcr.io/davidudell/persistent:latest /bin/bash

playwright install-deps

playwright install

cd src

export DISPLAY=:99

export OPENAI_API_KEY=<key_value>

Xvfb :99 -screen 0 1024x768x16 &

python3 browser_loop.py
```

## Project Status
An early stage WIP: 0.0.1
