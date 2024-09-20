# %%
"""
A persistent chatbot via system prompts, with brower API access.

Note that the sync playwright API will not run in a notebook environment.
"""


import os
from textwrap import dedent

import openai
from playwright.sync_api import sync_playwright

# %%
# Constants
openai.api_key = os.getenv("OPENAI_API_KEY")
SYSTEM_PROMPT: str = dedent(
    """
    You are an autonomous AI with browser access through the `playwright` API.
    """
)
text: dict = {
    "role": "system",
    "content": f"{SYSTEM_PROMPT}",
}


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
window.goto("https://www.google.com")

# %%
# Interaction loop
while True:
    pass