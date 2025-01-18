"""
A persistent AI agent via system prompts, with browser access.

Note that the `playwright` sync API used here will not run in a Jupyter
notebook.
"""

import os
from textwrap import dedent

from openai import OpenAI
from openai.types import Completion

from tiktoken import encoding_for_model
from utils.model_api import postprocess
from utils.p_wright import kickstart
from utils.state import exec_action, trim, Logs

SYSTEM_PROMPT: str = dedent(
    """
    You are an autonomous AI with browser access through the Python playwright
    API. Decide what to do next, then issue a command by replying with that
    command as a Python string. Remember to pass in commands without triple
    quotes or ticks: these strings will go into exec(). Commands are
    postprocessed with exactly the following:
    command = command.split("Command:")[-1].strip().replace("`", "'")
    So, don't reason out load after the string literal "Command:". Reason
    before that point then append at the very end:
    Command: your_command_here
    Note the absense of backticks.
    All state lives in the state object. Its page attribute is the current
    browser page, while the browser attribute is the browser itself. Execution
    ends when state.page is None or state.browser is None. You can assign
    either of those to None to end the loop. Be careful to always modify the
    attributes: the exec loop won't expose a variable like page or browser
    mutably. On the other hand, the attributes of state are mutable from within
    exec. You will receive page text content from now on as user responses. No
    outside human feedback will be provided.
    """
)
CONTEXT_LIMIT: int = 100000

client: OpenAI = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)
tokenizer = encoding_for_model("gpt-4")

page, browser = kickstart()
state: Logs = Logs(page, browser)

initial_log: dict = {
    "role": "system",
    "content": f"{SYSTEM_PROMPT}",
}
state.logs.append(initial_log)

while state.page is not None and state.browser is not None:
    state: Logs = trim(state, CONTEXT_LIMIT, tokenizer)
    response: Completion = client.chat.completions.create(
        messages=state.logs,
        model="gpt-4o",
    )
    processed: list[str] = postprocess(response)
    command: str = processed[-1]
    state: Logs = exec_action(command, state)
