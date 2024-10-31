"""Playwright sync utility functions."""


def kickstart(p_wright):
    """Start the playwright browser instance."""

    # headless=False to expose the browser window
    browser_out = p_wright.chromium.launch(
        headless=False,
        timeout=0,
    )
    profile = browser_out.new_context()
    page_out = profile.new_page()

    return page_out, browser_out
