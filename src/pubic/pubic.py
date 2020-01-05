# coding: utf-8
from pubic import auth
from pubic import storage


def _main():
    access_token, endpoint = auth.get_storage_credentials()
    contents = storage.list_container(endpoint, access_token, "default")
    print("/n".join(contents))


if __name__ == '__main__':
    _main()
