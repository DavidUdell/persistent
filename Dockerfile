# `greenlet` is not compatible with Python 3.13
FROM python:3.11

WORKDIR /app

COPY . /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential python3-dev xvfb
RUN pip install -U pip setuptools wheel
RUN pip install --no-cache-dir -U -e .
RUN playwright install-deps && playwright install
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["/bin/bash"]
