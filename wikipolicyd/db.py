"""Handles interaction with a simple key-value store."""

import datetime
from pathlib import Path

import pickledb  # type: ignore

_DB_DIR = Path('/var/lib/wikipolicyd')


class Db(object):
    """Persistent data storage interface.

    Client needs to keep track of how much data was already bought,
    so this information needs to be stored in DB.
    """
    def __init__(self, name: str):
        self._db = pickledb.load(_DB_DIR / name, auto_dump=True)

    def used_gb(self, date: datetime.date) -> int:
        """Read from DB the amount of GB bought for a certain date."""
        return self._db.get(self._gb_used_key(date), 0)

    def add_used_gb(self, date: datetime.date, gb: int = 1) -> None:
        """Update the amount of GB bought for a certain date."""
        cur_value = self.used_gb(date)
        if not self._db.set(self._gb_used_key(date), cur_value + gb):
            raise RuntimeError("Could not update DB after buying more data")

    def _gb_used_key(self, date: datetime.date) -> str:
        return 'gb_used:' + date.isoformat()
