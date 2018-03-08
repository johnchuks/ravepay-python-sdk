from resources import Create, List, Find
from utils.url_utils import merge_dict


class RaveDirectCharge(Create):

    @classmethod
    def create_payment(cls, payload, api):
        endpoint = '/charge'
        public_key_dict = dict(PBFPubKey=api.PUBLIC_KEY)
        new_payload = merge_dict(payload, public_key_dict)
        if new_payload:
            return cls.create(endpoint, api, new_payload)


class ValidateCardCharge(Create):
    @classmethod
    def post(cls, payload, api):
        endpoint = '/validatecharge'
        public_key_dict = dict(PBFPubKey=api.PUBLIC_KEY)
        revised_payload = merge_dict(payload, public_key_dict)
        request = cls.create(endpoint, api, revised_payload)
        return request
