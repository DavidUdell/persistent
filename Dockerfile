# syntax=docker/dockerfile:1.17.0
# `greenlet` is not compatible with Python 3.13
FROM python:3.12-slim-bookworm

# uv
COPY --from=ghcr.io/astral-sh/uv:0.8.3 /uv /uvx /bin/

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-dev xvfb

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv,sharing=locked \
    uv sync --locked --no-install-project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv,sharing=locked \
    uv sync --locked --no-editable

ENV PATH="/app/.venv/bin:$PATH"
RUN playwright install-deps && playwright install

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["/bin/bash"]
