"""Manually experimenting with `playwright`."""

from utils.state import exec_action, Logs
from utils.p_wright import kickstart


page, browser = kickstart()
logs: Logs = Logs(page, browser)

while True:
    command: str = input("$:")
    exec_action(command, logs)
