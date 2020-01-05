# coding: utf-8
import requests


def list_container(endpoint, access_token, name="default"):
    # Openstack from here
    print()
    print("# 5. Openstack APIs")
    print()

    headers = {
        "X-Auth-Token": f"{access_token}"
    }
    print(headers)
    response = requests.get(
        endpoint + "/" + name,
        headers=headers)
    print(response.status_code)

    if response.status_code != 200:
        print(response.reason)
        print(response.text)
        import pdb
        pdb.set_trace()

    return response.text.split("/n")
