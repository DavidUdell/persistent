"""
A persistent AI agent via system prompts, with browser access.

Note: the `playwright` sync API used herein will not run in a Jupyter notebook.
"""

import os
from textwrap import dedent

import openai
from openai.types import Completion
from playwright.sync_api import sync_playwright


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
    the browser instance itself. Execution ends when window is None.

    You will receive page text content from now on as user responses. No
    outside human feedback will be provided. Initial hardcoded commands start
    you at https://www.duckduckgo.com and read the whole page content. Why
    don't you try to navigate to a range of different pages?
    """
)

LAUNCH_SITE: str = "https://www.duckduckgo.com"

explainers_log: list[dict] = [
    {
        "role": "system",
        "content": f"{SYSTEM_PROMPT}",
    },
]


# Browser initialization functionality
def run(pwrite):
    """Run playwright browser setup."""

    # headless=True, the default, suppresses the actual browser window.
    browser_instance = pwrite.chromium.launch(
        headless=False,
        timeout=0,
    )
    profile = browser_instance.new_context()
    page_instance = profile.new_page()

    return page_instance, browser_instance


# Explanation action loop functionality
def action(
    explained_action: Completion,
    state_log: list[dict],
) -> list[dict]:
    """
    Post-process an explained action string, execute it, and return resulting
    contents.
    """
    command = explained_action.choices[0].message.content
    command = command.split("Command:")[-1]
    command = command.strip()
    command = command.replace("`", "'")

    try:
        content = exec(  # pylint: disable=exec-used
            command,
            globals(),
            locals(),
        )
    except Exception as e:  # pylint: disable=broad-except
        content = f"Caught: {e}"

    state_log.append(
        {
            "role": "user",
            "content": f"Command: {command}\n{content}",
        }
    )

    return state_log


# OpenAI client setup
# Remember to export the OPENAI_API_KEY env variable first.
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

window, browser = run(sync_playwright().start())

# Hardcoded Action 1
window.goto(LAUNCH_SITE)
explainers_log.append(
    {
        "role": "user",
        "content": f"Command: window.goto({LAUNCH_SITE})\n",
    }
)
print("Hardcoded Action 1:")
print(explainers_log[-1]["content"])
print()

# Hardcoded Action 2
page_content: str = window.content()
explainers_log.append(
    {
        "role": "user",
        "content": "Command: window.content()" + f"\n{page_content}",
    }
)
print("Hardcoded Action 2:")
print(explainers_log[-1]["content"])
print()

act_idx: int = 3

while window is not None:
    completion = client.chat.completions.create(
        messages=explainers_log,
        model="gpt-4o",
    )

    explainers_log = action(completion, explainers_log)

    print(f"Action {act_idx}:")
    print(explainers_log[-1]["content"])
    print()

    act_idx += 1

print()
print("Final log of agent actions:")
print()
for i in explainers_log:
    print(i["content"])
