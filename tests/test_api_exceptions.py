import unittest
from collections import namedtuple
from ravepaypysdk.api_exceptions import ApiError


class TestApiExceptions(unittest.TestCase):
    def setUp(self):
        self.Response = namedtuple('Response', 'status_code')

    def test_error_without_content(self):
        response = self.Response(status_code="404")
        print(self.Response)
        error = ApiError(response, content=None)
        self.assertEqual(str(error), "Error. Response status code: %s" % response.status_code)

    def test_error_with_content(self):
        response = self.Response(status_code="400")
        content = dict(error='You have a bug somewhere')
        error = ApiError(response, content=content)
        self.assertEqual(str(error), "Error. Response status code: {} Response content: {}" .format(response.status_code, content))

    def test_Error_without_response_or_content(self):
        error = ApiError({})
        self.assertEqual(str(error), "Error. ")
