# coding: utf-8
import argparse
import logging
import tabulate

from pubic import auth
from pubic import storage
from pubic._version import __version_text__


def _main():
    parser = argparse.ArgumentParser(
        description='''A terminal-based GUI client for Git.''')
    parser.add_argument(
        '-v', '--version', action='version', version=__version_text__)
    parser.parse_args()

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    access_token, endpoint = auth.get_storage_credentials()

    containers = storage.list_containers(endpoint, access_token)
    for c in containers:
        print(c)

    objects = storage.list_container(endpoint, access_token)
    search_results = [x for x in objects if ".gif" in x][:10]

    objects_properties = storage.stat_object_list(search_results, endpoint, access_token, container_name="default")
    headers = ["Name", "Last Modified", "Size (B)", "Type"]
    print(tabulate.tabulate(objects_properties, headers=headers))


if __name__ == '__main__':
    _main()
