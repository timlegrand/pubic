import os
import logging

from pubic import filesystem


def sync_folder(storage_client, sync_folder):
    # Get the list of files on the cloud
    cloud_files = storage_client.list_container()

    if not os.path.exists(sync_folder):
        print(f"Sync folder '{sync_folder}' does not exist. Creating...")
        os.mkdir(sync_folder)

    # Meanwhile, get the list of files on the disk (destination folder)
    local_files = list(filesystem.list_files(sync_folder))

    # Get list of files to download
    missing_local_files = list(set(cloud_files) - set(local_files))[:10]  # limit results to 10

    # Get list of files to upload
    missing_remote_files = list(set(local_files) - set(cloud_files))[:10]  # limit results to 10

    # Download missing local files
    for file_path in missing_local_files:
        if not file_path:
            continue

        dest_full_path = os.path.join(sync_folder, file_path)
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