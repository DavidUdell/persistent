"""Manually experimenting with `playwright`."""

from playwright.sync_api import sync_playwright


def action_like():
    """Test action-like function loop."""

    # Solicit input text
    input_text = input("$:")

    try:
        content = exec(  # pylint: disable=exec-used
            input_text,
            globals(),
            locals(),
        )
    except Exception as e:  # pylint: disable=broad-except
        content = e

    print(content)


def kickstart(pwriter):
    """Kickstart the browser."""
    browser_instance = pwriter.chromium.launch(
        headless=False,
        timeout=0,
    )
    profile = browser_instance.new_context()
    new_page = profile.new_page()

    return new_page, browser_instance


page, browser = kickstart(sync_playwright().start())
step: int = 0
while True:
    step += 1
    action_like()
    print(step)
