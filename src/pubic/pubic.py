# coding: utf-8
from pubic import auth
from pubic import storage

import logging
import tabulate


def _main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    access_token, endpoint = auth.get_storage_credentials()

    # containers = storage.list_containers(endpoint, access_token)
    # for c in containers:
    #     print(c)

    objects = storage.list_container(endpoint, access_token)
    search_results = [x for x in objects if ".gif" in x][:10]

    objects_properties = storage.stat_object_list(search_results, endpoint, access_token, container_name="default")
    headers = ["Name", "Last Modified", "Size (B)", "Type"]
    print(tabulate.tabulate(objects_properties, headers=headers))


if __name__ == '__main__':
    _main()
