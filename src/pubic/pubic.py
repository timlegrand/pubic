# coding: utf-8
import logging
import tabulate

from pubic import auth
from pubic import storage
from pubic import cli


def _main():
    args = cli.parse_cli_args()

    # Setup logging
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)

    # Authenticate against Hubic APIs
    access_token, endpoint = auth.get_storage_credentials()

    storage_client = storage.Client(endpoint, access_token)

    if args.list_containers:
        containers = storage_client.list_containers()
        for c in containers:
            print(c)

    if args.search_expr:
        objects = storage_client.list_container()
        search_results = [x for x in objects if args.search_expr in x]
        if args.limit:
            search_results = [x for x in objects if args.search_expr in x][:args.limit]
        objects_properties = storage_client.stat_object_list(search_results)
        if objects_properties:
            headers = ["Name", "Last Modified", "Size (B)", "Type"]
            print(tabulate.tabulate(objects_properties, headers=headers))
        else:
            print("No result.")


if __name__ == '__main__':
    _main()
