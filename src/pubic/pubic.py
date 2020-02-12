# coding: utf-8
import logging
import tabulate

from pubic import auth
from pubic import storage
from pubic import cli
from pubic import filesystem


def _main():
    args = cli.parse_cli_args()

    # Setup logging
    logging.basicConfig(
        format="[%(levelname)s] %(message)s",
        level=getattr(logging, args.log_level.upper()))

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
        import os

        # Get the list of files on the cloud
        cloud_files = storage_client.list_container()

        if not os.path.exists(args.sync_folder):
            print(f"Sync folder '{args.sync_folder}' does not exist. Creating...")
            os.mkdir(args.sync_folder)

        # Meanwhile, get the list of files on the disk (destination folder)
        local_files = list(filesystem.list_files(args.sync_folder))

        # Get list of files to download
        missing_local_files = list(set(cloud_files) - set(local_files))[:10]  # limit results to 10

        # Get list of files to upload
        missing_remote_files = list(set(local_files) - set(cloud_files))[:10]  # limit results to 10

        # Download missing local files
        for file_path in missing_local_files:
            if not file_path:
                continue

            dest_full_path = os.path.join(args.sync_folder, file_path)
            logging.warning(f"Downloading missing file {file_path} into {dest_full_path}")
            content, props = storage_client.download_object(file_path)

            if props["Content-Type"] == "application/directory":
                logging.warning("Creating pure directory " + file_path)
                os.makedirs(dest_full_path)
                continue

            dest_full_dirpath = os.path.dirname(dest_full_path)
            if not os.path.exists(dest_full_dirpath):
                logging.warning("Creating directory " + dest_full_dirpath)
                os.makedirs(dest_full_dirpath)
            with open(dest_full_path, "wb") as f:
                f.write(content)
        return

        # Meanwhile, upload missing files

        # Meanwhile, compute file list of changes or corruptions

        # Download these files


if __name__ == '__main__':
    _main()
