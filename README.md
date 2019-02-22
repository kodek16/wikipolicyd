# wikipolicyd

A simple daemon that helps controlling high-speed data policy
of [WikiLink](http://wikilink.by/), an ISP in Brest, Belarus.

## Installing

Use `sudo pip install .` for a system-wide install.

## Running

First, create `/var/lib/wikipolicyd` directory and assure
that it's owned by the user that's going to run the daemon.

Add configuration files to `/etc/wikipolicyd` directory:
- `credentials.toml`, which should have two keys: `login` and `password`
- `policy.toml`, with a single key of form `data_limit = "20G"`

You can also add a key of form `exception = "2019-01-02"` to `policy.toml`
to enable unlimited data for a given day.
