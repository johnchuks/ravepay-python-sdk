class Create(object):
    @classmethod
    def create(cls, endpoint, api, payload=None):
        if payload is not None:
            return api.post(endpoint, payload)


# class Find(object):
#     def find(self, params=None):
#         if params is not None:
#             return self.api.get(endpoint, params)
#         else:
#             return self.api.get(endpoint)


class List(object):
    @classmethod
    def list(cls, endpoint, api, params=None):
        print(api)
        if params is not None:
            return api.get(endpoint, params)
        elif params is None:
            print('i am here')
            return api.get(endpoint)


# class Update(object):
#     def update(self, payload):
#         return self.api.put(endpoint, payload)
