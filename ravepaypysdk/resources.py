class Create(object):
    @classmethod
    def create(cls, endpoint, api, payload=None):
        if payload is not None:
            return api.post(endpoint, payload)


class Find(object):
    def find(self, params=None):
        if params is not None:
            return self.api.get(endpoint, params)
        else:
            return self.api.get(endpoint)


class List(object):
    def list(self, params):
        if params is not None:
            return self.api.get(endpoint, params)


class Update(object):
    def update(self, payload):
        return self.api.put(endpoint, payload)
