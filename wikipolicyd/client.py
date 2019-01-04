"""Client runs continuosly and interacts with WikiLink admin settings.

Client enforces the policy from the configuration files.
"""

import datetime
import logging
import sched

from wikipolicyd.db import Db
from wikipolicyd.policy import Policy
from wikipolicyd.settings_server import SettingsServer


logger = logging.getLogger(__name__)


class Client(object):
    _CHECK_INTERVAL_S = 30

    def __init__(self, db: Db, policy: Policy, settings: SettingsServer):
        self.db = db
        self.policy = policy
        self.settings = settings
        self.scheduler = sched.scheduler()

    def run(self) -> None:
        self.scheduler.enter(0, 1, self.check)
        self.scheduler.run()

    def check(self) -> None:
        today = datetime.date.today()
        no_high_speed_data = self.settings.get_remaining_mb()
        enough_money = (
                self.settings.get_balance() > self.settings.get_turbo_price())

        max_turbo_gb = self.policy.data_limit(today)
        if max_turbo_gb:
            max_turbo_gb -= self.settings.get_included_free_gb()
            policy_allows_turbo = (
                    self.db.used_gb(today) + self.settings.get_turbo_gb()
                    < max_turbo_gb)
        else:
            policy_allows_turbo = True

        if no_high_speed_data and enough_money and policy_allows_turbo:
            if max_turbo_gb:
                logger.info('Activating turbo: %d GB used, policy allows %d',
                            self.db.used_gb(today),
                            max_turbo_gb)
            else:
                logger.info('Activating turbo: %d GB used, exception active',
                            self.db.used_gb(today))
            self.settings.activate_turbo()
            self.db.add_used_gb(today, self.settings.get_turbo_gb())

        self.scheduler.enter(self._CHECK_INTERVAL_S, 1, self.check)
