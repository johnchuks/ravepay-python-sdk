""" Module for various utility or service functions"""

import json
import re
from .encryption import encrypt_data


SANDBOX = 'https://ravesandboxapi.flutterwave.com'
LIVE = 'https://api.ravepay.co'


def get_url(mode):
    """ Function for getting URL based on mode"""
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
    public_key_algo_type_dict = dict(PBFPubKey=api.public_key, alg='3DES-24')
    encrypt_payload = encrypt_data(api.secret_key, stringify_payload)
    encrypt_payload_dict = dict(client=encrypt_payload)
    new_payload = merge_dict(encrypt_payload_dict, public_key_algo_type_dict)
    return new_payload
