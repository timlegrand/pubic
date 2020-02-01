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
