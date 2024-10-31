"""
A persistent AI agent via system prompts, with browser access.

Note that the `playwright` sync API used here will not run in a Jupyter
notebook.
"""

import os
from textwrap import dedent

from openai import OpenAI
from openai.types import Completion

from utils.model_api import postprocess
from utils.p_wright import kickstart
from utils.state import exec_action, Logs


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

    The page object is the current browser page, while the browser object is
    the browser itself. Execution ends when state.page is None or
    state.browser is None. You can assign either of those to None to end the
    loop.

    You will receive page text content from now on as user responses. No
    outside human feedback will be provided.
    """
)

client: OpenAI = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

page, browser = kickstart()
state: Logs = Logs(page, browser)

initial_log: dict = {
    "role": "system",
    "content": f"{SYSTEM_PROMPT}",
}
state.logs.append(initial_log)

while page.window is not None and page.browser is not None:
    response: Completion = client.chat.completions.create(
        messages=state.logs,
        model="gpt-4o",
    )
    processed: list[str] = postprocess(response)
    command: str = processed[-1]
    state: Logs = exec_action(command, state)
