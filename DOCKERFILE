FROM python:latest

WORKDIR /app

# Not root user
RUN groupadd --system ai_agent_group && useradd --system ai_agent --group ai_agent_group

COPY . /app
RUN pip install --no-cache-dir -e .

# Change to non-root user
USER ai_agent

# Run the application.
CMD ["python3", "src/browser_loop.py"]
