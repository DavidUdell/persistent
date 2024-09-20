# %%
"""
A persistent chatbot via system prompts, with brower API access.

Note that the sync playwright API will not run in a notebook environment.
"""


import os

import openai
from playwright.sync_api import sync_playwright

# %%
# Constants
openai.api_key = os.getenv("OPENAI_API_KEY")
# System prompt
messages: dict = {
    "role": "system",
    "content": """You are an AI with `playwright` API browser access.""",
}


# %%
# Browser setup
def run(pwrite):
    """Run playwright browser setup."""

    browser = pwrite.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.google.com")
    print((page.title()))

    browser.close()


run(sync_playwright().start())

# %%
# Interaction loop
