import os
import re
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

secure_mode = os.environ.get('MODE')
SANDBOX = 'http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/flwv3-pug/getpaidx/api/'
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
