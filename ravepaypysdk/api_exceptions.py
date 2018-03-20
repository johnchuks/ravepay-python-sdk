""" Exception module for returning error message
from RavePay"""

class ApiError(object):
    """Error Class"""

    def __init__(self, response, content=None):
        """initialize attributes for the class"""
        self.response = response
        self.content = content

    def __str__(self):
        """convert object to string"""
        error_message = 'Error. '
        if hasattr(self.response, 'status_code'):
            error_message += "Response status code: {}".format(self.response.status_code)
        if self.content is not None:
            error_message += " Response content: {}".format(self.content)
        return error_message
