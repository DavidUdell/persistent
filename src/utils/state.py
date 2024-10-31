"""State management utilities."""

from dataclasses import dataclass, field

from playwright.sync_api import Browser, Page


@dataclass
class Logs:
    """Logs state management, always in the global scope."""

    page: Page
    browser: Browser
    step: int = 0
    logs: list[dict] = field(default_factory=list)


def exec_action(
    command: str,
    state: Logs,
) -> Logs:
    """Execute, log, and print a model command."""

    try:
        content: str | None = exec(  # pylint: disable=exec-used
            command,
            globals(),
            locals(),
        )
        content: str = "" if content is None else content
        content += state.page.content()

    except Exception as exception:  # pylint: disable=broad-except
        content: str = f"Caught: {exception}"

    log: dict = {
        "role": "user",
        "content": f"Command: {command}\nContent: {content}",
    }

    print(log["content"])
    state.logs.append(log)

    return state
