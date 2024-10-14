# `greenlet` is not compatible with Python 3.13
FROM python:3.11

WORKDIR /app

# Not root user
RUN groupadd --system ai_agent_group && useradd --system ai_agent --group ai_agent_group

COPY . /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential python3-dev xvfb
RUN pip install -U pip setuptools wheel
RUN pip install --no-cache-dir -U -e .
RUN playwright install-deps
RUN playwright install

# Change to non-root user
# USER ai_agent

# For `Xvfb`
ENV DISPLAY=:99
