"""Interface with the OpenAI API."""

from openai.types import Completion


def postprocess(
    response: Completion,
    word_of_power: str = "Command:",
) -> list[str]:
    """
    Postprocess a model response for execution and logging; print non-commands.

    Non-final element in the list are any thinking out loud, while the final
    element is an exec-ready command.
    """

    response_content = response.choices[0].message.content
    split_content = response_content.split(word_of_power)

    split_content[-1] = split_content[-1].strip().replace("`", "'")

    for i in split_content[:-1]:
        print(i)

    return split_content
