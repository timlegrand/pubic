# coding: utf-8
import requests
import logging


def list_containers(endpoint, access_token):
    logging.info(f"Listing containers...")

    headers = { "X-Auth-Token": f"{access_token}" }
    logging.debug(headers)

    response = requests.get(
        endpoint + "/",
        headers=headers)
    logging.debug(response.status_code)

    if response.status_code != 200:
        logging.debug(response.reason)
        logging.debug(response.text)
        import pdb
        pdb.set_trace()

    return response.text.split("\n")


def list_container(endpoint, access_token, container_name="default"):
    logging.info(f"Listing '{container_name}' container...")

    headers = { "X-Auth-Token": f"{access_token}" }
    logging.debug(headers)

    response = requests.get(
        endpoint + "/" + container_name,
        headers=headers)
    logging.debug(response.status_code)

    if response.status_code != 200:
        logging.debug(response.reason)
        logging.debug(response.text)
        import pdb
        pdb.set_trace()

    return response.text.split("\n")


def stat_object(endpoint, access_token, container_name="default", object_path=""):
    logging.debug(f"Stating '{container_name}/{object_path}'...")

    headers = { "X-Auth-Token": f"{access_token}" }
    logging.debug(headers)

    response = requests.head(
        endpoint + "/" + container_name + "/" + object_path,
        headers=headers)
    logging.debug(response.status_code)

    if response.status_code != 200:
        logging.debug(response.reason)
        logging.debug(response.text)

    return response.headers
