"""Top-level script that runs the client."""

import logging

from wikipolicyd.db import Db
from wikipolicyd.client import Client
from wikipolicyd.policy import Policy
from wikipolicyd.settings_server import RealWikilinkSettingsServer


def main():
    logging.basicConfig(level=logging.DEBUG)

    db = Db('data')
    policy = Policy()
    settings = RealWikilinkSettingsServer()
    client = Client(db, policy, settings)
    client.run()


if __name__ == '__main__':
    main()
