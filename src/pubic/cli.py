import argparse

from pubic._version import __version_text__


def parse_cli_args():

    # Handle CLI arguments
    parser = argparse.ArgumentParser(description="""Pubic, the Hubic cloud storage client made reliable.""")
    parser.add_argument("--version", action="version", version=__version_text__)
    parser.add_argument("--list-containers", action="store_true", default=False, help="list containers")
    parser.add_argument("--quotas", action="store_true", default=False, help="show storage stats and quotas")
    parser.add_argument("--limit", type=int, default=10, help="limit for search results (default 10, 0 means no limit)")
    parser.add_argument("--search", dest="search_expr",  help="search for files matching the given expression")
    parser.add_argument("--download", dest="download_path",  help="download a specific file")
    parser.add_argument("--destination",  help="destination for downloaded content")
    parser.add_argument("--sync-folder",  help="folder to sync the remote with (safe for cloud - download only)")
    parser.add_argument("--log-level", default="WARNING", help="set log level to one of CRITICAL, ERROR, WARNING, INFO, DEBUG (default: WARNING)")
    return parser.parse_args()
