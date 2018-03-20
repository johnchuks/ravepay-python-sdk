import unittest
from unittest.mock import patch
from ravepaypysdk.helpers import Create, List
from ravepaypysdk.api import Api


class TestCreate(unittest.TestCase):
    def setUp(self):
        self.api = Api(
            secret_key='dummy',
            public_key='dummy',
            production=False
        )
        self.endpoint = '/'
        self.payload = dict(name='Ravepay')

    @patch('ravepaypysdk.api.Api.post')
    def test_create_method(self, mock):
        self.create = Create.create(self.endpoint, self.api, self.payload)
        mock.assert_called_once_with(self.endpoint, self.payload)


class TestList(unittest.TestCase):
    def setUp(self):
        self.api = Api(
            secret_key='dummy',
            public_key='dummy',
            production=False
        )
        self.endpoint = '/'
        self.payload = dict(name='Ravepay')

    @patch('ravepaypysdk.api.Api.get')
    def test_list_with_params(self, mock):
        params=dict(id='2')
        self.list_with_params = List.list(self.endpoint, self.api, params=params)
        mock.assert_called_once_with(self.endpoint, params)

    @patch('ravepaypysdk.api.Api.get')
    def test_list_without_params(self, mock):
        self.list_with_params = List.list(self.endpoint, self.api, params=None)
        mock.assert_called_once_with(self.endpoint)
