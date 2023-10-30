# Copyright (C) 2023 Nicolas Da Mutten
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import asyncio
import logging

from argparse_logging import add_logging_arguments

from cli.daemon import Daemon
from reader import Reader


def add_read_command(parser_group):
    parser_group.add_parser(
        name="read",
        help="Read Data",
        description="Reads the Devices and uploads it to influxdb",
    )


def main():
    parser = argparse.ArgumentParser(
        description="Read SmartGadget Values and upload to InfluxDB"
    )

    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    add_logging_arguments(parser)

    subparsers = parser.add_subparsers(
        dest="subparser",
        description="Use the following subcommands to perform the actions once. "
        "If omitted, the reader runs in daemon mode, "
        "automatically reading data based on schedule",
    )

    add_read_command(subparsers)

    args = parser.parse_args()

    reader = Reader()

    if "subparser" in args and args.subparser is not None:
        if args.subparser == "read":

            async def run_once():
                await reader.read()
                await reader.close()

            try:
                asyncio.run(run_once())
            except (KeyboardInterrupt, SystemExit):
                pass
    else:
        daemon = Daemon(reader)
        daemon.main()


if __name__ == "__main__":
    main()
