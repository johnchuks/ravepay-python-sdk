"""
This module contains the default API
object for the SDK. It contains the request handlers and
response handler respectively
"""

import json

import requests

from ravepaypysdk.api_exceptions import ApiError
from ravepaypysdk.utils.rave_utils import get_url, merge_url


class Api(object):
    """
    Default Object for RavePay Api
    """
    secret_key = None
    public_key = None

    def __init__(self, **kwargs):
        self.secret_key = kwargs.get('secret_key')
        self.public_key = kwargs.get('public_key')
        self.mode = kwargs.get('production')
        self.title = '**RavePayPYSDK**'
        self.payload = None
        self.query_string = None

        if not self.mode:
            self.url = get_url(mode='sandbox')
        else:
            self.url = get_url(mode='live')

    def __repr__(self):
        return "{}".format(self.title)

    @staticmethod
    def handle_response(response, content):
        """Validate HTTP Response"""
        status = response.status_code

        if status == 200 or status == 201:
            response = dict(status_code=status, content=json.loads(content))
            if content:
                return response
        elif status == 400:
            api_error = ApiError(response, content)
            return api_error

    def request(self, method, url, **kwargs):
        """handles request to RavePay API"""
        http_header = dict(content_type='application/json')

        self.payload = kwargs.get('payload')
        self.query_string = kwargs.get('params')
        if self.payload is not None and self.query_string is None:
            response = requests.request(
                method, url, data=self.payload, headers=http_header)
            print(response.content.decode('utf-8'))
            return Api.handle_response(response, response.content.decode('utf-8'))

        if self.payload is None and self.query_string is None:
            response = requests.request(method, url, headers=http_header)
            return Api.handle_response(response, response.content.decode('utf-8'))

        if self.query_string is not None and self.payload is None:
            response = requests.request(
                method, url, headers=http_header, params=self.query_string)
            return Api.handle_response(response, response.content.decode('utf-8'))

    def get(self, endpoint, query_string=None):
        """
        Make a GET Request
        """

        if query_string is not None:
            return self.request(
                'GET', merge_url(self.url, endpoint),
                payload=None, params=query_string)
        return self.request(
            'GET', merge_url(self.url, endpoint),
            payload=None, params=None
        )

    def post(self, endpoint, payload):
        """
        Make a POST Request
        """
        return self.request(
            'POST',
            merge_url(self.url, endpoint), payload=payload
        )

    def put(self, endpoint, payload, query_string=None):
        """
        Make a PUT Request
        """
        return self.request(
            'PUT',
            merge_url(self.url, endpoint),
            payload=payload, params=query_string
        )
