"""Policy defines the behavior of the client.

Policy is read from configuration files and defines when the client
should perform an action (e.g. press the "turbo" button).
"""

import datetime
import re
from typing import Optional

from wikipolicyd.config import ConfigFile


class Policy(object):
    def __init__(self, read_config: bool = True, **kwargs):
        if not read_config:
            self._data_limit_gb = kwargs['data_limit_gb']  # type: int
            self._exception_date = kwargs.get('exception_date', None)
            return

        config = ConfigFile('policy')
        data_limit = str(config['data_limit'])
        if not re.match(r'^\d+G$', data_limit):
            raise RuntimeError(
                    'Policy file must have a "stream.data_limit" key '
                    + ' which is a number with "G" suffix')

        self._data_limit_gb = int(data_limit[:-1])
        if self._data_limit_gb <= 0:
            raise RuntimeError('Data limit must be a positive value')

        self._exception_date = None  # type: Optional[datetime.date]
        if 'exception' in config:
            self._exception_date = datetime.datetime.strptime(
                    config['exception'], '%Y-%m-%d').date()

    def data_limit(self, date: datetime.date) -> Optional[int]:
        if (self._exception_date
                and self._exception_date == date):
            return None
        return self._data_limit_gb
