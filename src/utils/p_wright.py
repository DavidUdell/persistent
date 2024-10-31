"""Playwright sync utility functions."""

from playwright.sync_api import Browser, Page, Playwright, sync_playwright


def kickstart() -> tuple[Page, Browser]:
    """Start a playwright browser and page."""

    playwright: Playwright = sync_playwright().start()
    # `headless=False` here to expose the browser window
    browser: Browser = playwright.chromium.launch(
        headless=False,
        timeout=0,
    )
    page = browser.new_page()

    return (page, browser)
