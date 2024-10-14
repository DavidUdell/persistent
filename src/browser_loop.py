"""
A persistent AI agent via system prompts, with browser API access.

Note: the sync playwright API will not run in a notebook environment.
"""

import os
from textwrap import dedent

import openai
from playwright.sync_api import sync_playwright


# Constants
SYSTEM_PROMPT: str = dedent(
    """
    You are an autonomous AI with browser access through the `playwright` API.

    Decide what to do next, then issue a command from the following list by
    replying with that command as a string:

    -

    You will receive page text content from now on as user responses.
    """
)

state_log: list[dict] = [
    {
        "role": "system",
        "content": f"{SYSTEM_PROMPT}",
    },
]


# Browser setup functionality
def run(pwrite):
    """Run playwright browser setup."""

    # headless=True, the default, suppresses the actual browser window.
    browser_instance = pwrite.chromium.launch(headless=False)
    profile = browser_instance.new_context()
    page_instance = profile.new_page()

    return page_instance


# OpenAI client setup
# Remember to export the OPENAI_API_KEY env variable first.
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Interaction loop
if True:  # pylint: disable=using-constant-test
    # Launch browser
    window = run(sync_playwright().start())

    # In-place navigation
    SITE: str = "https://www.duckduckgo.com"
    command_str: str = f"Command: window.goto({SITE})"
    window.goto(SITE)
    command_dict: dict = {
        "role": "user",
        "content": command_str,
    }
    state_log.append(command_dict)

    content: list[str] | str = window.locator("p").all_inner_texts()
    if isinstance(content, list):
        content: str = "\n".join(content)
    command_str: str = (
        "Command: `\\n`.join(window.locator('p').all_inner_texts())"
    )
    content_dict: dict = {
        "role": "user",
        "content": command_str + "\n" + content,
    }
    state_log.append(content_dict)

    for d in state_log:
        assert isinstance(d, dict)
        assert "role" in d
        assert "content" in d
        assert d["role"] in ["system", "user", "assistant"]

    completion = client.chat.completions.create(
        messages=state_log,
        model="gpt-4o-mini",
    )

    print(completion.choices[0].message.content)

    new_command = completion.choices[0].message.content
    new_command = new_command.split("Command:")[-1].strip()

    # Execute the command. Hillariously insecure; this should live in a
    # container, really, at least.
    try:
        new_input = exec(  # pylint: disable=exec-used
            new_command,
            globals(),
            locals(),
        )
    except Exception as e:  # pylint: disable=broad-except
        new_input = f"Caught: {e}"
    print(new_input)
