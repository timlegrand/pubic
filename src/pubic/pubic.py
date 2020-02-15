# coding: utf-8
import tabulate

from pubic import auth
from pubic import storage
from pubic import cli
from pubic import sync
from pubic import logs


def _main():
    args = cli.parse_cli_args()

    # Setup logging
    logger = logs.setup_logger(args)

    # Authenticate against Hubic APIs
    storage_client = storage.Client()

    if args.list_containers:
        containers = storage_client.list_containers()
        for c in containers:
            print(c)

    if args.search_expr:
        objects = storage_client.list_container()
        search_results = [x for x in objects if args.search_expr in x]  # TODO: use pathlib.Path.rglob
        if args.limit:
            search_results = [x for x in objects if args.search_expr in x][:args.limit]
        objects_properties = storage_client.stat_object_list(search_results)
        if objects_properties:
            headers = ["Name", "Last Modified", "Size (B)", "Type"]
            print(tabulate.tabulate(objects_properties, headers=headers))
        else:
            print("No result.")

    if args.download_path:
        content = storage_client.download_object(args.download_path)
        destination = args.destination or os.path.basename(args.download_path)
        with open(destination, "wb") as f:
            f.write(content)

    if args.sync_folder:
        sync.sync_folder(storage_client, args.sync_folder)


if __name__ == '__main__':
    _main()
