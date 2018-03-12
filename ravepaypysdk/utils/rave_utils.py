import json
import re
from utils.encryption import encrypt_data


SANDBOX = 'http://flw-pms-dev.eu-west-1.elasticbeanstalk.com'
LIVE = 'https://api.ravepay.co'


def get_url(mode):
    if mode == 'sandbox':
        return SANDBOX

    elif mode == 'live':
        return LIVE


def merge_url(url, *url_paths):
    """
    Utility function for merging url paths
    """
    for path in url_paths:
        url = re.sub(r'/?$', re.sub(r'^/?', '/', path), url)
    return url


def merge_dict(data, *override):
    """
    Utility function for merging dictionaries
    """
    result = {}
    for current_dict in (data,) + override:
        result.update(current_dict)
    return result


def initialize_config(payload, api):
    """
    Function for initializing payload for Rave direct charge
    """
    stringify_payload = json.dumps(payload)
    public_key_algo_type_dict = dict(PBFPubKey=api.PUBLIC_KEY, alg='3DES-24')
    encrypt_payload = encrypt_data(api.SECRET_KEY, stringify_payload)
    encrypt_payload_dict = dict(client=encrypt_payload)
    new_payload = merge_dict(encrypt_payload_dict, public_key_algo_type_dict)
    return new_payload
