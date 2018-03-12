import unittest
from collections import namedtuple
from ravepaypysdk.api_exceptions import ApiError


class TestApiExceptions(unittest.TestCase):

    def setUp(self):
        self.Response = namedtuple('Response', 'status_code')

    def test_not_found(self):
        response = self.Response(status_code="404")
        print(self.Response)
        error = ApiError(response, content=None)
        self.assertEqual(repr(error), "Error. Response status code: %s" %(response.status_code))

    def test_connection(self):
        error = ApiError({})
        self.assertEqual(repr(error), "Error. ")