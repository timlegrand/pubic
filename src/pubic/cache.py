import logging
import os


def load_storage_credentials(storage_credentials_file='storage_credentials.txt'):
    try:
        with open(storage_credentials_file) as f:
            logging.info(f"Using cached storage credentials from: {storage_credentials_file}")
            storage_access_token = f.readline().rstrip('\n')
            storage_endpoint = f.readline().rstrip('\n')
        return storage_access_token, storage_endpoint
    except FileNotFoundError:
        return None
    except Exception as e:
        logging.info(f"Unable to get cached storage credentials from: {storage_credentials_file}: {e}")


def save_storage_credentials(storage_access_token, storage_endpoint, storage_credentials_file='storage_credentials.txt'):
    with open(storage_credentials_file, 'w') as f:
        logging.debug(f"Caching storage credentials into: {storage_credentials_file}")
        f.write(storage_access_token + "\n")
        f.write(storage_endpoint + "\n")


def reset_storage_credentials(storage_credentials_file='storage_credentials.txt'):
    try:
        os.remove(storage_credentials_file)
    except Exception as e:
        logging.info(f"Error trying removing {storage_credentials_file}: {e}")
        return
    logging.info(f"Removed storage credentials: {storage_credentials_file}")


def load_api_credentials(api_credentials_file='api_credentials.txt'):
    try:
        with open(api_credentials_file) as f:
            logging.info(f"Using cached API credentials from: {api_credentials_file}")
            api_access_token = f.readline().rstrip('\n')
            api_refresh_token = f.readline().rstrip('\n')
        return api_access_token, api_refresh_token
    except:
        logging.info(f"Unable to use cached API credentials file: {api_credentials_file}")
        return None


def save_api_credentials(api_access_token, api_refresh_token, api_credentials_file='api_credentials.txt'):
    with open(api_credentials_file, 'w') as f:
        logging.debug(f"Caching API credentials into: {api_credentials_file}")
        f.write(api_access_token + "\n")
        f.write(api_refresh_token + "\n")


def reset_api_credentials(api_credentials_file='api_credentials.txt'):
    try:
        os.remove(api_credentials_file)
    except Exception as e:
        logging.info(f"Error trying removing {api_credentials_file}: {e}")
        return
    logging.info(f"Removed API credentials: {api_credentials_file}")
