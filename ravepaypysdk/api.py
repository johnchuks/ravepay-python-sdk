import requests
import json
from utils.url_utils import get_url, merge_url
from api_exceptions import ApiError
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

    def __repr__(self):
        return "{}{}".format(self.mode, self.PUBLIC_KEY)


    def request(self, method, url, payload=None, params=None):
        http_header = dict(content_type='application/json')
        if payload is not None:
            print()
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
            raise ApiError(response, content)

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
        return self.request('POST', merge_url(self.url, endpoint), payload)

    def put(self, endpoint, payload):
        """
        Make a PUT Request
        """
        return self.request(merge_url(self.url, endpoint), 'PUT', payload)

    def patch(self, endpoint, payload):
        return self.request(merge_url(self.url, endpoint), 'PATCH', payload)
