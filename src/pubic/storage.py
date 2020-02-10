# coding: utf-8
import requests
import logging
import datetime
import time

from requests.exceptions import *

from pubic import auth
from pubic import req


MAX_RETRY = 3

class AuthenticationException(Exception):
    pass

class UnauthorizedException(AuthenticationException):
    pass


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
            except UnauthorizedException:
                self.authenticate(use_cache=False)
            except ConnectionError as e:
                #Exception
                # print(e)
                logging.error("Please check your Internet connection.")
            except:
                print("Oops!")

            time.sleep(1)
            retry += 1

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

        object_data = response.headers
        object_last_modified = datetime.datetime.strptime(object_data["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z")
        # store_time = datetime.datetime.fromtimestamp(int(float(object_data["X-Timestamp"])))
        # print(object_last_modified.strftime('%Y-%m-%d %H:%M:%S'))
        # print(store_time.strftime('%Y-%m-%d %H:%M:%S'))
        object_size = object_data["Content-Length"]
        object_type = object_data["Content-Type"]
        object_properties = (
            object_name,
            object_last_modified,
            object_size,
            object_type
        )
        return objects_properties


    def download_object(self, object_path="", container_name="default"):
        logging.debug(f"Downloading '{container_name}/{object_path}'...")

        headers = { "X-Auth-Token": f"{self.access_token}" }
        logging.debug(headers)

        response = requests.get(
            self.endpoint + "/" + container_name + "/" + object_path,
            headers=headers)
        logging.debug(response.status_code)

        if response.status_code != 200:
            logging.debug(response.reason)
            logging.debug(response.text)

        return response.content


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
