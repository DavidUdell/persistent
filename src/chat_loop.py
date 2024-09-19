# %%
"""A persistent chatbot via system prompts, with brower API access."""


import os

import openai
from playwright.sync_api import sync_playwright

# %%
# Constants.
openai.api_key = os.getenv("OPENAI_API_KEY")
