# %%
"""
A persistent chatbot via system prompts, with brower API access.

Note: the sync playwright API will not run in a notebook environment.
"""


import os
from textwrap import dedent

import openai
from playwright.sync_api import sync_playwright

# %%
# Constants
SYSTEM_PROMPT: str = dedent(
    """
    You are an autonomous AI with browser access through the `playwright` API.

    Decide what to do next, then issue a command from the following list by
    replying with that command as a string:

    -

    You will receive page text content from now on as a response.
    """
)
state_log: list[dict] = [
    {
        "role": "system",
        "content": f"{SYSTEM_PROMPT}",
    },
]

# %%
# OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")
# client = openai.OpenAI()


# %%
# Browser setup functionality
def run(pwrite):
    """Run playwright browser setup."""

    # headless=True, the default, suppresses the actual browser window.
    browser_instance = pwrite.chromium.launch(headless=False)
    profile = browser_instance.new_context()
    page_instance = profile.new_page()

    return page_instance


# %%
# Launch browser
window = run(sync_playwright().start())

# In-place navigation
SITE: str = "https://www.duckduckgo.com"
window.goto(SITE)

command_dict: dict = {
    "role": "command",
    "content": f"window.goto({SITE})",
}
state_log.append(command_dict)

content: list[str] | str = window.locator("p").all_inner_texts()
if isinstance(content, list):
    content: str = "\n".join(content)

content_dict: dict = {
    "role": "'\\n.'.join(window.locator('p').all_inner_texts())",
    "content": content,
}
state_log.append(content_dict)

for i in state_log:
    print(i)

# %%
# Interaction loop
# while True:
# pass

# Model
