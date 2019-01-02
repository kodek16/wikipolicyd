"""Client runs as a daemon and interacts with WikiLink admin settings.

Client enforces the policy from the configuration files.
"""

from wikipolicyd.policy import Policy
from wikipolicyd.settings_server import SettingsServer


class Client(object):
    def __init__(self, policy: Policy, settings: SettingsServer):
        self.policy = policy
        self.settings = settings
