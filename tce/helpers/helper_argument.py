import argparse

import logging

logger = logging.getLogger(__name__)


def get_arguments(arguments):
    argument_parser = argparse.ArgumentParser(
        description="Script to download travian classements",
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999),
    )

    argument_parser.add_argument(
        "-i",
        "--identifiant",
        required=True,
        help="""Travian identifiant (username or email)
Required to get classements
Example : python tce/main.py -i myusername""",
        type=str,
    )

    argument_parser.add_argument(
        "-p",
        "--password",
        required=True,
        help="""Travian password
Required to get classements
Example : python tce/main.py -p mypassword""",
        type=str,
    )

    argument_parser.add_argument(
        "-d",
        "--driver",
        required=True,
        help="""
Chrome web driver
Example : python tce/main.py -d C:\chromedriver.exe""",
        type=str,
    )

    argument_parser.add_argument(
        "-v",
        "--verbose",
        help="""Active verbose mode, support different level
Example : python japscandownloader/main.py -v""",
        action="count",
    )

    argument_parser.add_argument(
        "-s",
        "--server",
        help="""Server number (login page order)
Example : python japscandownloader/main.py -s 0
For the first server on login page""",
        type=str,
    )

    return argument_parser.parse_args(arguments)
