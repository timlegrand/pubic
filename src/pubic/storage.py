# coding: utf-8
import requests
import logging
import datetime

from pubic import req


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


def stat_object_list(
    object_list,
    endpoint,
    access_token,
    container_name="default",
    object_path=""):
    """Get metadata for every object path provided in object_list."""

    objects_props = []
    objects_props = req.run_async(
        req.stat_objects,
        object_list,
        endpoint,
        access_token,
        container_name="default")

    objects_properties = []
    for p, object_name in objects_props:
        object_data = p
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
    return objects_properties
