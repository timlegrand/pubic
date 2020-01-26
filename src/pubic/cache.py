import logging


def get_storage_credentials(storage_credentials_file='storage_credentials.txt'):
    try:
        with open(storage_credentials_file) as f:
            logging.info(f"Using cached credentials from: {storage_credentials_file}")
            storage_access_token = f.readline().rstrip('\n')
            storage_endpoint = f.readline().rstrip('\n')
        return storage_access_token, storage_endpoint
    except:
        logging.INFO(f"Unable to use cached credentials file: {storage_credentials_file}")
        return None


def save_storage_credentials(storage_access_token, storage_endpoint, storage_credentials_file='storage_credentials.txt'):
    with open(storage_credentials_file, 'w') as f:
        logging.debug(f"Caching credentials into: {storage_credentials_file}")
        f.write(storage_access_token + "\n")
        f.write(storage_endpoint + "\n")
