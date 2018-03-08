import requests
import json
from utils.url_utils import get_url, merge_url
import exceptions
import os


class Api(object):
    SECRET_KEY = None
    PUBLIC_KEY = None

    def __init__(self, secret_key, public_key, production):
        self.SECRET_KEY = secret_key
        self.PUBLIC_KEY = public_key
        self.mode = production

        if not self.mode:
            self.url = get_url(mode='sandbox')
        else:
            self.url = get_url(mode='live')

    def request(self, method, url, payload, params=None):
        http_header = dict(content_type='application/json')
        if method == 'POST' or method == 'PUT' or method == 'PATCH':
            response = requests.request(method, url, data=payload, headers=http_header)
        else:
            response = requests.request(method, url, headers=http_header)

        if params is not None:
            response = requests.request(method, url, params, headers=http_header)
        return self.handle_response(response, response.content.decode('utf-8'))

    def handle_response(self, response, content):
        """
        Validate HTTP Response
        :param response: response object
        :param content: response content
        :return: response status and object
        """
        status = response.status_code

        if status == 200:
            return json.loads(content) if content else {}
        elif status == 400:
            raise exceptions.ApiErrors(response, content)

    def get(self, endpoint, params=None):
        """
        Make a GET Request
        """
        if params is not None:
            return self.request(merge_url(self.url, endpoint), 'GET', params)
        else:
            return self.request(merge_url(self.url, endpoint), 'GET')

    def post(self, endpoint, payload):
        """
        Make a POST Request
        """
        return self.request(merge_url(self.url, endpoint), 'POST', payload)

    def put(self, endpoint, payload):
        """
        Make a PUT Request
        """
        return self.request(merge_url(self.url, endpoint), 'PUT', payload)

    def patch(self, endpoint, payload):
        return self.request(merge_url(self.url, endpoint), 'PATCH', payload)


rave_api = None

def default_object():
    """
    Returns the default Api object and if it is not present creates a new one
    :return:
    """
    global rave_api
    if rave_api is None:
        try:
            secret_key = os.environ.get('SECRET_KEY')
            public_key = os.environ.get('PUBLIC_KEY')
        except KeyError:
            msg = 'RavePay PUBLIC KEY and SECRET  are required'
            raise KeyError(msg)
        rave_api = Api(secret_key=secret_key, public_key=public_key, production=False)
    return rave_api
