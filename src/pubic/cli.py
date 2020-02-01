import argparse

from pubic._version import __version_text__


def parse_cli_args():

    # Handle CLI arguments
    parser = argparse.ArgumentParser(description="""Pubic, the Hubic cloud storage client made reliable.""")
    parser.add_argument("-v", "--version", action="version", version=__version_text__)
    parser.add_argument("--list-containers", action="store_true", default=False, help="list containers")
    parser.add_argument("--limit", type=int, default=10, help="limit for search results (default 10, 0 means no limit)")
    parser.add_argument("--search", dest="search_expr",  help="search for files matching the given expression")
    return parser.parse_args()

