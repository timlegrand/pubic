# coding: utf-8
import argparse
import logging
import tabulate

from pubic import auth
from pubic import storage
from pubic._version import __version_text__


def _main():
    # Handle CLI arguments
    parser = argparse.ArgumentParser(description="""Pubic, the Hubic cloud storage client made reliable.""")
    parser.add_argument("-v", "--version", action="version", version=__version_text__)
    parser.add_argument("--list-containers", action="store_true", default=False, help="list containers")
    parser.add_argument("--limit", type=int, default=10, help="limit for search results (default 10, 0 means no limit)")
    parser.add_argument("--search", dest="search_expr",  help="search for files matching the given expression")
    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)

    # Authenticate against Hubic APIs
    access_token, endpoint = auth.get_storage_credentials()

    if args.list_containers:
        containers = storage.list_containers(endpoint, access_token)
        for c in containers:
            print(c)

    if args.search_expr:
        objects = storage.list_container(endpoint, access_token)
        search_results = [x for x in objects if args.search_expr in x]
        if args.limit:
            search_results = [x for x in objects if args.search_expr in x][:args.limit]
        objects_properties = storage.stat_object_list(
            search_results,
            endpoint,
            access_token,
            container_name="default")
        if objects_properties:
            headers = ["Name", "Last Modified", "Size (B)", "Type"]
            print(tabulate.tabulate(objects_properties, headers=headers))
        else:
            print("No result.")


if __name__ == '__main__':
    _main()
