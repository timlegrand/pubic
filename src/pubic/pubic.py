# coding: utf-8
import pubic.auth

import requests


def _main():
    access_token, endpoint = pubic.auth.get_storage_credentials()

    # Openstack from here
    print()
    print("# 5. Openstack APIs")
    print()

    headers = {
        "X-Auth-Token": f"{access_token}"
    }
    print(headers)
    response = requests.get(
        endpoint + "/default",
        headers=headers)
    print(response.status_code)

    if response.status_code != 200:
        print(response.reason)
        print(response.text)
        import pdb
        pdb.set_trace()
    print("/n".join(response.text.split("/n")))


if __name__ == '__main__':
    _main()
