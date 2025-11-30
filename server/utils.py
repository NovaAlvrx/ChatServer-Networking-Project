# server/utils.py
import logging

# === Color constants for server console ===
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"


def color(text: str, code: str) -> str:
    return f"{code}{text}{RESET}"


# === Logging helpers ===

def setup_logging() -> None:
    """
    Configure basic logging to server.log.
    """
    logging.basicConfig(
        filename="server.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def log_info(msg: str) -> None:
    logging.info(msg)


def log_error(msg: str) -> None:
    logging.error(msg)
