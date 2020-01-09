# coding: utf-8
from pubic import auth
from pubic import storage

import logging
import datetime
import tabulate


def _main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    access_token, endpoint = auth.get_storage_credentials()

    containers = storage.list_containers(endpoint, access_token)
    for c in containers:
        print(c)

    contents = storage.list_container(endpoint, access_token)
    search_results = [x for x in contents if ".gif" in x]
    objects_properties = []
    for i, object_name in enumerate(search_results):
        object_data = storage.stat_object(endpoint, access_token, "default", object_name)
        object_last_modified = datetime.datetime.strptime(object_data["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z")
        # store_time = datetime.datetime.fromtimestamp(int(float(object_data["X-Timestamp"])))
        # print(object_last_modified.strftime('%Y-%m-%d %H:%M:%S'))
        # print(store_time.strftime('%Y-%m-%d %H:%M:%S'))
        object_size = object_data["Content-Length"]
        object_type = object_data["Content-Type"]
        objects_properties.append((
            object_name,
            object_last_modified,
            object_size,
            object_type
        ))
        if i > 10:
            break
    print("Search result (only 10 firsts)")
    headers = ["Name", "Last Modified", "Size (B)", "Type"]
    print(tabulate.tabulate(objects_properties, headers=headers))


if __name__ == '__main__':
    _main()
