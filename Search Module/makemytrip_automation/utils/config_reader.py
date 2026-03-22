"""
utils/config_reader.py
Reads configuration values from config/config.yaml
"""

import os
import yaml
from pathlib import Path


class ConfigReader:
    """Singleton config reader — loads YAML once, exposes helper properties."""

    _instance = None
    _config: dict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        """Locate and parse config.yaml relative to the project root."""
        root = Path(__file__).resolve().parent.parent
        config_path = root / "config" / "config.yaml"
        with open(config_path, "r") as f:
            self._config = yaml.safe_load(f)

    # ------------------------------------------------------------------ #
    # Browser
    # ------------------------------------------------------------------ #
    @property
    def browser(self) -> str:
        return self._config["browser"]["name"].lower()

    @property
    def headless(self) -> bool:
        return self._config["browser"]["headless"]

    @property
    def window_size(self) -> str:
        return self._config["browser"]["window_size"]

    @property
    def implicit_wait(self) -> int:
        return int(self._config["browser"]["implicit_wait"])

    # ------------------------------------------------------------------ #
    # Application
    # ------------------------------------------------------------------ #
    @property
    def base_url(self) -> str:
        return self._config["application"]["base_url"]

    @property
    def timeout(self) -> int:
        return int(self._config["application"]["timeout"])

    @property
    def page_load_timeout(self) -> int:
        return int(self._config["application"]["page_load_timeout"])

    # ------------------------------------------------------------------ #
    # Credentials
    # ------------------------------------------------------------------ #
    @property
    def username(self) -> str:
        return self._config["credentials"]["username"]

    @property
    def password(self) -> str:
        return self._config["credentials"]["password"]

    @property
    def mobile(self) -> str:
        return self._config["credentials"]["mobile"]

    # ------------------------------------------------------------------ #
    # Search data helpers
    # ------------------------------------------------------------------ #
    def get_flight_data(self) -> dict:
        return self._config["search_data"]["flight"]

    def get_hotel_data(self) -> dict:
        return self._config["search_data"]["hotel"]

    def get_bus_data(self) -> dict:
        return self._config["search_data"]["bus"]

    # ------------------------------------------------------------------ #
    # Paths
    # ------------------------------------------------------------------ #
    @property
    def screenshots_path(self) -> str:
        return self._config["paths"]["screenshots"]

    @property
    def reports_path(self) -> str:
        return self._config["paths"]["reports"]

    @property
    def logs_path(self) -> str:
        return self._config["paths"]["logs"]

    # ------------------------------------------------------------------ #
    # Raw access (fallback)
    # ------------------------------------------------------------------ #
    def get(self, *keys, default=None):
        """Navigate nested keys: config.get('search_data', 'flight', 'from_city')"""
        value = self._config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, default)
            else:
                return default
        return value
