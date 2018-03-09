import os
import re
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SANDBOX = 'http://flw-pms-dev.eu-west-1.elasticbeanstalk.com'
LIVE = 'https://api.ravepay.co/flwv3-pug/getpaidx/api/'


def get_url(mode):
    if mode == 'sandbox':
        return SANDBOX

    elif mode == 'live':
        return LIVE


def merge_url(url, *url_paths):
    for path in url_paths:
        url = re.sub(r'/?$', re.sub(r'^/?', '/', path), url)
    return url

def merge_dict(data, *override):
    result = {}
    for current_dict in (data,) + override:
        result.update(current_dict)
    return result
