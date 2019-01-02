"""Utilities for working with configuration files."""

from pathlib import Path

import toml

_CONFIG_DIR = Path('/etc/wikipolicyd')


class ConfigFile(dict):
    """Represents a single configuration file."""

    def __init__(self, name: str):
        """Loads a configuration file with a given name."""
        self.name = name
        file_path = _CONFIG_DIR / (name + ".toml")
        with file_path.open() as f:
            super().__init__(**toml.load(f))
