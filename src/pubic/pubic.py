# coding: utf-8
import logging
import tabulate

from pubic import auth
from pubic import storage
from pubic import cli


import os

def list_files(path):
    local_tree = os.walk(path)
    for dirpath, dirnames, filenames in local_tree:
        for dirname in dirnames:
            yield (os.path.join(dirpath, dirname) + "/")[len(path) + 1:]
        for filename in filenames:
            yield (os.path.join(dirpath, filename))[len(path) + 1:]


def _main():
    args = cli.parse_cli_args()

    # Setup logging
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)

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
        # Get the list of files on the cloud

        cloud_files = storage_client.list_container()
        # for o in cloud_files:
        #     print(o)
        # return

        # (fake cloud with local source folder)
        # cloud_files = list(list_files("toto"))
        # print("Cloud files:")
        # for filename in cloud_files:
        #     print(filename)
        # print()

        if not os.path.exists(args.sync_folder):
            print(f"Sync folder '{args.sync_folder}' does not exist. Creating...")
            os.mkdir(args.sync_folder)

        # Meanwhile, get the list of files on the disk (destination folder)
        local_files = list(list_files(args.sync_folder))
        print("Local files:")
        for filename in local_files:
            print(filename)
        print()

        # Get list of files to download
        missing_local_files = list(set(cloud_files) - set(local_files))
        print("Missing local files:")
        import copy
        missing_local_files = missing_local_files[:10]
        for f in missing_local_files:
            print(f)
        print()

        # Get list of files to upload
        missing_remote_files = list(set(local_files) - set(cloud_files))
        print("Missing remote files:")
        for f in missing_remote_files:
            print(f)
        print()

        # Download missing files
        print("Downloading missing files:")
        for file_path in missing_local_files:
            if not file_path:
                continue

            # For fake cloud only
            if file_path.endswith("/"):
                logging.warning("Creating directory " + file_path)
                # os.mkdir(file_path)
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
