"""
A persistent AI agent via system prompts, with browser access.

Note: the `playwright` sync API used herein will not run in a Jupyter notebook.
"""

import os
from textwrap import dedent

import openai
from playwright.sync_api import sync_playwright

from utils.playwright import kickstart
from utils.update_state import take_action


# Constants
SYSTEM_PROMPT: str = dedent(
    """
    You are an autonomous AI with browser access through the Python playwright
    API.
    
    Decide what to do next, then issue a command by replying with that command
    as a Python string. Remember to pass in commands without triple quotes or
    ticks: these strings will go into exec(). Commands are postprocessed with
    the following:

    command = command.split("Command:")[-1]
    command = command.strip()
    command = command.replace("`", "'")

    So, _don't_ reason out load after the string literal "Command:". Reason
    _before_ that point then pass "Command: your_command_here" when ready.

    The window object is the current browser page, while the browser object is
    the browser instance itself. Execution ends when state["window"] is None or
    state["browser"] is None. You can assign either of those to None to end the
    loop; note the state dict, to work around access through exec().

    You will receive page text content from now on as user responses. No
    outside human feedback will be provided.
    """
)

logs: list[dict] = [
    {
        "role": "system",
        "content": f"{SYSTEM_PROMPT}",
    },
]


# OpenAI client setup
# Remember to export the OPENAI_API_KEY env variable first.
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

state: dict = {
    "window": None,
    "browser": None,
}
state["window"], state["browser"] = kickstart(sync_playwright().start())

step: int = 1
while (state["window"] is not None) and (state["browser"] is not None):
    reply = client.chat.completions.create(
        messages=logs,
        model="gpt-4o",
    )

    logs = take_action(reply, logs)

    print(f"Step {step}:")
    print(logs[-1]["content"], end="\n\n")

    step += 1

print("\n", f"Logs end: {step} steps taken.")
