"""Handles interaction with a simple persistent store."""

import datetime
import os
from pathlib import Path
import shelve

_DB_DIR = Path('/var/lib/wikipolicyd')


class Db(object):
    """Persistent data storage interface.

    Client needs to keep track of how much data was already bought,
    so this information needs to be stored in DB.
    """
    def __init__(self, name: str):
        if not _DB_DIR.is_dir():
            raise RuntimeError('{} must be a directory'.format(_DB_DIR))

        if _DB_DIR.owner() != os.environ.get('USER'):
            raise RuntimeError('{} must be owned by user running wikipolicyd'
                               .format(_DB_DIR))

        os.makedirs(_DB_DIR, exist_ok=True)
        self._db = shelve.open(str(_DB_DIR / name))

    def used_gb(self, date: datetime.date) -> int:
        """Read from DB the amount of GB bought for a certain date."""
        try:
            return self._db[self._gb_used_key(date)]
        except KeyError:
            return 0

    def add_used_gb(self, date: datetime.date, gb: int = 1) -> None:
        """Update the amount of GB bought for a certain date."""
        cur_value = self.used_gb(date)
        self._db[self._gb_used_key(date)] = cur_value + gb

    def _gb_used_key(self, date: datetime.date) -> str:
        return 'gb_used:' + date.isoformat()
