# coding: utf-8
from pubic import auth
from pubic import storage

import logging
import datetime


def _main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    access_token, endpoint = auth.get_storage_credentials()

    containers = storage.list_containers(endpoint, access_token)
    for c in containers:
        print(c)

    contents = storage.list_container(endpoint, access_token)
    search_results = [x for x in contents if ".jpg" in x]
    for r in search_results:
        print(r)
        object_data = storage.stat_object(endpoint, access_token, "default", r)
        print(object_data["Last-Modified"])
        print(datetime.datetime.fromtimestamp(int(float(object_data["X-Timestamp"]))).strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    _main()
