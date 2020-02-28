# coding: utf-8
import requests
import logging
import datetime
import time

from requests.exceptions import *

from pubic import auth
from pubic import req


MAX_RETRY = 3


def parse_metadata(headers, path=""):
    props = {}
    if path:
        props["path"] = path
    if "Last-Modified" in headers:  # May not be present
        props["last-modified"] = datetime.datetime.strptime(headers["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z")
    if "X-Timestamp" in headers:  # May not be present
        props["store-time"] = datetime.datetime.fromtimestamp(int(float(headers["X-Timestamp"])))
    if "Content-Length" in headers:  # Mandatory
        props["size"] = int(headers["Content-Length"])
    if "Content-Type" in headers:  # Mandatory
        props["type"] = headers["Content-Type"]

    return props


class Client:
    def __init__(self, endpoint=None, access_token=None):
        self.endpoint = endpoint
        self.access_token = access_token
        if not self.access_token or not self.endpoint:
            self.authenticate()

        retry = 0
        data = []
        while not data and retry < MAX_RETRY:
            try:
                data = self.list_containers()
            except auth.UnauthorizedException:
                self.authenticate(use_cache=False)
            except ConnectionError as e:
                #Exception
                # print(e)
                logging.error("Please check your Internet connection.")
            except:
                print("Oops!")

            time.sleep(1)
            retry += 1

        if not self.endpoint or not self.access_token:
            raise auth.AuthenticationException("Cannot get authentication information")

    def authenticate(self, use_cache=True):
        try:
            self.access_token, self.endpoint = auth.get_storage_credentials(use_cache)
        except ConnectionError:
            logging.error("Server unreachable.")

    def list_containers(self):
        logging.info(f"Listing containers...")

        headers = { "X-Auth-Token": f"{self.access_token}" }
        logging.debug(headers)

        response = requests.get(
            self.endpoint + "/",
            headers=headers)
        logging.debug(response.status_code)

        if response.status_code != 200:
            logging.debug(response.reason)
            logging.debug(response.text)
            if response.status_code == 401 and response.reason == "Unauthorized":
                raise UnauthorizedException()
            # import pdb
            # pdb.set_trace()

        return response.text.split("\n")


    def list_container(self, container_name="default"):
        logging.info(f"Listing '{container_name}' container...")

        headers = { "X-Auth-Token": f"{self.access_token}" }
        logging.debug(headers)

        response = requests.get(
            self.endpoint + "/" + container_name,
            headers=headers)
        logging.debug(response.status_code)

        if response.status_code != 200:
            logging.debug(response.reason)
            logging.debug(response.text)

        return response.text.split("\n")


    def stat_object(self, container_name="default", object_path=""):
        logging.debug(f"Stating '{container_name}/{object_path}'...")

        headers = { "X-Auth-Token": f"{self.access_token}" }
        logging.debug(headers)

        response = requests.head(
            self.endpoint + "/" + container_name + "/" + object_path,
            headers=headers)
        logging.debug(response.status_code)

        if response.status_code != 200:
            logging.debug(response.reason)
            logging.debug(response.text)

        metadata = parse_metadata(response.headers, object_path)
        return metadata


    def download_object(self, object_path="", container_name="default"):
        logging.debug(f"Downloading '{container_name}/{object_path}'...")

        headers = { "X-Auth-Token": f"{self.access_token}" }
        logging.debug(headers)

        response = requests.get(
            self.endpoint + "/" + container_name + "/" + object_path,
            headers=headers)
        logging.debug(response.status_code)

        if response.status_code != 200:
            logging.warning(f"Error trying to download '{object_path}': {response.reason} (status code {response.status_code})")
            return None, parse_metadata(response.headers, object_path)

        return response.content, parse_metadata(response.headers, object_path)


    def stat_object_list(
        self,
        object_list,
        container_name="default",
        object_path=""):
        """Get metadata for every object path provided in object_list."""

        objects_props = []
        objects_props = req.run_async(
            req.stat_objects,
            object_list,
            self.endpoint,
            self.access_token,
            container_name="default")

        objects_properties = []
        for props, object_name in objects_props:
            objects_properties.append(parse_metadata(props, object_name))
        return objects_properties
