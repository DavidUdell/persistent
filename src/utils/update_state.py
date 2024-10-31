"""State management utilities."""

from textwrap import dedent

from openai.types import Completion


def take_action(
    unparsed_action: Completion,
    running_logs: list[dict],
) -> list[dict]:
    """Postprocess and execute a model action."""
    raw = unparsed_action.choices[0].message.content
    split = raw.split("Command:")

    for comment in split:
        print(comment)

    # Postprocess
    command = split[-1]
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

    running_logs.append(
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

    return running_logs
