"""Top-level script that runs the client."""

import logging

import click

from wikipolicyd.db import Db
from wikipolicyd.client import Client
from wikipolicyd.policy import Policy
from wikipolicyd.settings_server import RealWikilinkSettingsServer


@click.command()
def main():
    """Simple daemon for controlling Wikilink data policy."""
    logging.basicConfig(level=logging.DEBUG)

    db = Db('data')
    policy = Policy()
    settings = RealWikilinkSettingsServer()
    client = Client(db, policy, settings)
    client.run()


if __name__ == '__main__':
    main()
