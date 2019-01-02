"""Abstraction for a remote WikiLink settings interface."""

from abc import ABCMeta, abstractmethod
import math
import re
import time

import requests

from wikipolicyd.config import ConfigFile


class SettingsServer(object, metaclass=ABCMeta):
    @abstractmethod
    def get_balance(self) -> int:
        """Returns account balance in BYN kopeikas."""

    @abstractmethod
    def get_plan_name(self) -> str:
        """Returns the name of the active plan."""

    @abstractmethod
    def get_remaining_mb(self) -> int:
        """Returns the remaining high-speed data amount for Stream plans."""

    @abstractmethod
    def activate_turbo(self) -> None:
        """Activates the "turbo" button, buying more high-speed data."""


class RealWikilinkSettingsServer(SettingsServer):
    """Settings provider that connects to the real WikiLink server."""

    # Don't refresh data if less than X seconds have passed.
    _REFRESH_FREQUENCY_S = 1.0

    _BALANCE_RE = re.compile(r'счете:(.*?)(?P<target>\d+,\d+)')
    _PLAN_RE = re.compile(
            r'<font color="\#4c4c4c"><span>\s+(?P<target>.*)\s+</span></font>')
    _REMAINING_MB_RE = re.compile(
            r'Осталось скоростного трафика:(.*?)(?P<target>\d+(\.\d)?)')

    def __init__(self):
        credentials = ConfigFile('credentials')
        self.username = credentials['login']
        self.password = credentials['password']
        self._refresh_data()

    def _should_refresh_data(self) -> bool:
        return time.time() - self._last_update_time > self._REFRESH_FREQUENCY_S

    def _refresh_data(self) -> None:
        res = requests.post(
                'http://cab.wikilink.by/sessions.php',
                data={
                    'user[redirect]': '',
                    'user_account': self.username,
                    'user_password': self.password,
                    'commit': 'Войти',
                })
        self._last_update_time = time.time()

        res.encoding = 'utf8'
        body = res.text

        balance_match = self._BALANCE_RE.search(body)
        if balance_match:
            balance = balance_match.group('target')
            rubles, kopeikas = balance.split(',')
            self.balance = int(rubles) * 100 + int(kopeikas)
        else:
            raise RuntimeError('Could not parse account balance')

        plan_match = self._PLAN_RE.search(body)
        if plan_match:
            self.plan = plan_match.group('target')
        else:
            raise RuntimeError('Could not parse traffic plan')

        remaining_mb_match = self._REMAINING_MB_RE.search(body)
        if remaining_mb_match:
            self.remaining_mb = math.ceil(
                    float(remaining_mb_match.group('target')))
        else:
            raise RuntimeError(
                    'Could not parse remaining high-speed data amount')

    def get_balance(self) -> int:
        if self._should_refresh_data():
            self._refresh_data()
        return self.balance

    def get_plan_name(self) -> str:
        if self._should_refresh_data():
            self._refresh_data()
        return self.plan

    def get_remaining_mb(self) -> int:
        if self._should_refresh_data():
            self._refresh_data()
        return self.remaining_mb

    def activate_turbo(self) -> None:
        pass
