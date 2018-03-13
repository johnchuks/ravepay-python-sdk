
class Create(object):
    """
    Utility for class for POST rest service
    """

    @classmethod
    def create(cls, endpoint, api, payload=None):
        """
        Process POST REST operations
        """
        if payload is not None:
            return api.post(endpoint, payload)


class List(object):
    """
    Utility for class for GET rest service
    """

    @classmethod
    def list(cls, endpoint, api, params=None):
        """
        Process GET rest operations
        """
        if params is not None:
            return api.get(endpoint, params)
        elif params is None:
            return api.get(endpoint)
