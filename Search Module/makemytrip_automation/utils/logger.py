"""
utils/logger.py
Centralised logging setup — call get_logger(__name__) in every module.
"""

import logging
import os
from pathlib import Path
from utils.config_reader import ConfigReader

_cfg = ConfigReader()


def get_logger(name: str = "makemytrip") -> logging.Logger:
    """
    Return a named logger.  Handlers are added only once to avoid
    duplicate log entries when the function is called multiple times.

    Args:
        name: Logger name (usually __name__ of the calling module).

    Returns:
        Configured logging.Logger instance.
    """
    logger = logging.getLogger(name)

    # Return early if handlers are already attached
    if logger.handlers:
        return logger

    level = getattr(logging, _cfg.get("logging", "level", default="INFO").upper(), logging.INFO)
    logger.setLevel(level)

    fmt = logging.Formatter(
        fmt="%(asctime)s  [%(levelname)-8s]  %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ── Console handler ────────────────────────────────────────────────
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # ── File handler (created only when configured) ────────────────────
    if _cfg.get("logging", "log_to_file", default=True):
        log_dir = Path(_cfg.logs_path)
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "test_execution.log"
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    # Prevent messages from propagating to root logger
    logger.propagate = False
    return logger
