# coding: utf-8
from pubic import auth
from pubic import storage
from pubic import req

import logging
import datetime
import tabulate
import time


def _main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    access_token, endpoint = auth.get_storage_credentials()

    # containers = storage.list_containers(endpoint, access_token)
    # for c in containers:
    #     print(c)

    contents = storage.list_container(endpoint, access_token)
    search_results = [x for x in contents if ".gif" in x][:10]

    print("Search result (only 10 firsts) - Async")
    t0 = time.time()
    objects_props = []
    objects_props = req.run_all(search_results, endpoint, access_token, container_name="default")
    objects_properties = []
    for p in objects_props:
        object_data = p
        object_last_modified = datetime.datetime.strptime(object_data["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z")
        # store_time = datetime.datetime.fromtimestamp(int(float(object_data["X-Timestamp"])))
        # print(object_last_modified.strftime('%Y-%m-%d %H:%M:%S'))
        # print(store_time.strftime('%Y-%m-%d %H:%M:%S'))
        object_size = object_data["Content-Length"]
        object_type = object_data["Content-Type"]
        objects_properties.append((
            "object_name",  #TODO: store object name along with async task and match result
            object_last_modified,
            object_size,
            object_type
        ))
    print(f"Time : {time.time() - t0:.2f}")

    print("Search result (only 10 firsts)")
    headers = ["Name", "Last Modified", "Size (B)", "Type"]
    print(tabulate.tabulate(objects_properties, headers=headers))

    print()

    print("Search result (only 10 firsts) - Sync")
    # Sequential execution for reference
    t0 = time.time()
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
    print(f"Time : {time.time() - t0:.2f}")

    print("Search result (only 10 firsts)")
    headers = ["Name", "Last Modified", "Size (B)", "Type"]
    print(tabulate.tabulate(objects_properties, headers=headers))


if __name__ == '__main__':
    _main()
