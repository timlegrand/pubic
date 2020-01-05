# coding: utf-8
import requests
import logging


def list_container(endpoint, access_token, name="default"):
    # Openstack from here
    logging.info("# 5. Openstack APIs")

    headers = {
        "X-Auth-Token": f"{access_token}"
    }
    logging.debug(headers)
    response = requests.get(
        endpoint + "/" + name,
        headers=headers)
    logging.debug(response.status_code)

    if response.status_code != 200:
        logging.debug(response.reason)
        logging.debug(response.text)
        import pdb
        pdb.set_trace()

    return response.text.split("/n")
