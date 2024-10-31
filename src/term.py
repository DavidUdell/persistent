"""Manual terminal into `playwright` interface."""

from utils.p_wright import kickstart
from utils.state import exec_action, Logs


page, browser = kickstart()
logs: Logs = Logs(page, browser)

while True:
    command: str = input("$:")
    exec_action(command, logs)
