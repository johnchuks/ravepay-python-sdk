import requests
import json
from ravepaypysdk.utils.rave_utils import get_url, merge_url
from ravepaypysdk.api_exceptions import ApiError


# noinspection PyMethodMayBeStatic
class Api(object):
    """
    Default Object for RavePay Api
    """
    SECRET_KEY = None
    PUBLIC_KEY = None

    def __init__(self, **kwargs):
        self.SECRET_KEY = kwargs.get('secret_key')
        self.PUBLIC_KEY = kwargs.get('public_key')
        self.mode = kwargs.get('production')
        self.title = 'RavePayAPI'

        if not self.mode:
            self.url = get_url(mode='sandbox')
        else:
            self.url = get_url(mode='live')

    def __repr__(self):
        return "{}".format(self.title)

    def request(self, method, url, **kwargs):
        """
        handles request to RavePay API

        """
        http_header = dict(content_type='application/json')

        payload = kwargs.get('payload')
        query_string = kwargs.get('params')
        if payload is not None and query_string is None:
            response = requests.request(
                method, url, data=payload, headers=http_header)
            return self.handle_response(response, response.content.decode('utf-8'))

        if payload is None and query_string is None:
            response = requests.request(method, url, headers=http_header)
            return self.handle_response(response, response.content.decode('utf-8'))

        if query_string is not None and payload is None:
            response = requests.request(
                method, url, headers=http_header, params=query_string)
            return self.handle_response(response, response.content.decode('utf-8'))

    def handle_response(self, response, content):
        """Validate HTTP Response"""
        status = response.status_code

        if status == 200:
            return json.loads(content) if content else {}
        elif status == 400:
            api_error = ApiError(response, content)
            return api_error

    def get(self, endpoint, query_string=None):
        """
        Make a GET Request
        """

        if query_string is not None:
            return self.request('GET', merge_url(self.url, endpoint), payload=None, params=query_string)
        else:
            return self.request('GET', merge_url(self.url, endpoint), payload=None, params=None)

    def post(self, endpoint, payload):
        """
        Make a POST Request
        """
        # print(merge_url(self.url,endpoint), payload, 'we are here bro')
        return self.request('POST', merge_url(self.url, endpoint), payload=payload)

    def put(self, endpoint, payload, query_string=None):
        """
        Make a PUT Request
        """
        return self.request('PUT', merge_url(self.url, endpoint), payload, params=query_string)

