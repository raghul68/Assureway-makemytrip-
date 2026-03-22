"""
utils/logger.py
─────────────────────────────────────────────────────────────────────────────
Centralised logging configuration for the MakeMyTrip automation framework.

Usage:
    from utils.logger import get_logger
    log = get_logger(__name__)
    log.info("Step description")
    log.error("Something went wrong")
"""

import logging
import os
from datetime import datetime

# ── Directory setup ──────────────────────────────────────────────────────────
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# ── Log file name (one file per run, timestamped) ────────────────────────────
_log_filename = os.path.join(
    LOGS_DIR, f"execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)

# ── Root logger configuration (called once at import) ───────────────────────
def _configure_root_logger() -> None:
    """Set up handlers on the root logger (idempotent)."""
    root = logging.getLogger()
    if root.handlers:
        return  # Already configured; avoid duplicate handlers

    root.setLevel(logging.DEBUG)

    # ── Console handler (INFO and above) ─────────────────────────────────────
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_fmt = logging.Formatter(
        fmt="%(asctime)s [%(levelname)-8s] %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )
    console_handler.setFormatter(console_fmt)

    # ── File handler (DEBUG and above — captures everything) ─────────────────
    file_handler = logging.FileHandler(_log_filename, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(
        fmt="%(asctime)s [%(levelname)-8s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_fmt)

    root.addHandler(console_handler)
    root.addHandler(file_handler)


# Initialise on first import
_configure_root_logger()


def get_logger(name: str) -> logging.Logger:
    """
    Return a named child logger.

    Args:
        name: Typically ``__name__`` of the calling module.

    Returns:
        A configured :class:`logging.Logger` instance.
    """
    return logging.getLogger(name)
