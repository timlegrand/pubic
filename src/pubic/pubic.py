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
            data = map(lambda x: (x["path"], x["last-modified"], x["size"], x["type"]), objects_properties)
            print(tabulate.tabulate(data, headers=headers))
        else:
            print("No result.")

    if args.download_path:
        content, props = storage_client.download_object(args.download_path)
        if props == None or props["Content-Type"] == "application/directory":
            return
        destination = args.destination or os.path.basename(args.download_path)
        with open(destination, "wb") as f:
            f.write(content)

    if args.sync_folder:
        sync.sync_folder(storage_client, args.sync_folder)

    if args.quotas:
        objects = storage_client.list_container()
        objects_properties = storage_client.stat_object_list(objects)
        total_size = sum(p["size"] for p in objects_properties)
        # total_size = 7015477674  # for testing purpose
        print(f"Total size (on remote): {float(total_size) / 1024 ** 3:.2f} GB")
        # print(f"Total size (local copy): {total_size}")


if __name__ == '__main__':
    _main()
