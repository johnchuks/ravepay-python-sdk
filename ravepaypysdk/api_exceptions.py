
class ApiError(object):
    def __init__(self, response, content=None):
        self.response = response
        self.content = content

    def __str__(self):
        """
        convert object to string
        :return:
        """
        error_message = 'Error. '
        if hasattr(self.response, 'status_code'):
            error_message += "Response status code: {}".format(self.response.status_code)
        if self.content is not None:
            error_message += " Response content: {}".format(self.content)
        return error_message


