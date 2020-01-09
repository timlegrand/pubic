# coding: utf-8
from pubic import auth
from pubic import storage

import logging


def _main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    access_token, endpoint = auth.get_storage_credentials()

    containers = storage.list_containers(endpoint, access_token)
    for c in containers:
        print(c)


if __name__ == '__main__':
    _main()
