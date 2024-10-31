"""State management utilities."""

from textwrap import dedent
from dataclasses import dataclass

from openai.types import Completion
from playwright.sync_api import Browser, Page


@dataclass
class Logs:
    """Logs state management, always in the global scope."""

    logs: list[dict] = []
    step: int = 0
    page: Page
    browser: Browser


def take_action(
    response: Completion,
    state: Logs,
) -> list[dict]:
    """Postprocess and execute a model action."""

    response_text = response.choices[0].message.content
    split_text = response_text.split("Command:")

    for comment in split_text:
        print(comment)

    # Postprocessing for exec
    command = split_text[-1]
    command = command.strip()
    command = command.replace("`", "'")

    try:
        exec(  # pylint: disable=exec-used
            command,
            globals(),
            locals(),
        )
        content = state

    except Exception as e:  # pylint: disable=broad-except
        content = f"Caught: {e}"

    state.append(
        {
            "role": "user",
            "content": dedent(
                f"""
                Command: {command}
                Exec content: {content}
                Page content: {state["window"].content()}
                """
            ),
        }
    )

    return state
