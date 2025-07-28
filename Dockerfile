# syntax=docker/dockerfile:1.17.0
ARG UV_VERSION=0.8.3
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uvbin

# `greenlet` is not compatible with Python 3.13
FROM python:3.12-slim-bookworm AS deps
COPY --from=uvbin /uv /uvx /bin/
WORKDIR /app

# apt
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update && apt-get install -y --no-install-recommends \
        build-essential python3-dev xvfb \
    && rm -rf /var/lib/apt/lists/*

# Python packages
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv,sharing=locked \
    uv sync --locked --no-install-project

# Playwright
ENV PLAYWRIGHT_BROWSERS_PATH=/root/.cache/ms-playwright \
    PATH="/app/.venv/bin:$PATH"
RUN --mount=type=cache,target=/root/.cache/ms-playwright,sharing=locked \
    playwright install-deps && playwright install chromium

# src
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv,sharing=locked \
    uv sync --locked --no-editable

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["/bin/bash"]
