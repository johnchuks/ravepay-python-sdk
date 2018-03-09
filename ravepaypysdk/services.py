import json
from resources import Create, List
from utils.url_utils import merge_dict
from utils.encryption import encrypt_data


class Card(Create):
    endpoint = '/flwv3-pug/getpaidx/api/charge'

    @classmethod
    def config(cls, payload, api):
        stringified_payload = json.dumps(payload)
        public_key_algo_type_dict = dict(PBFPubKey=api.PUBLIC_KEY, alg='3DES-24')
        encrypt_payload = encrypt_data(api.SECRET_KEY, stringified_payload)
        encrypt_payload_dict = dict(client=encrypt_payload)
        new_payload = merge_dict(encrypt_payload_dict, public_key_algo_type_dict)
        return new_payload

    @classmethod
    def rave_direct_charge(cls, payload, api):
        new_payload = cls.config(payload, api)
        if new_payload:
            return cls.create(cls.endpoint, api, new_payload)

    @classmethod
    def preauth_card(cls, payload, api):
        preauth_payload = cls.config(payload, api)
        if preauth_payload:
            return cls.create(cls.endpoint, api, preauth_payload)


class ValidateCharge(Create):
    @classmethod
    def card(cls, payload, api):
        endpoint = '/flwv3-pug/getpaidx/api/validatecharge'
        public_key_dict = dict(PBFPubKey=api.PUBLIC_KEY)
        revised_payload = merge_dict(payload, public_key_dict)
        request = cls.create(endpoint, api, revised_payload)
        return request

    @classmethod
    def account(cls, payload, api):
        account_endpoint = '/flwv3-pug/getpaidx/api/validate'
        public_key_dict = dict(PBFPubKey=api.PUBLIC_KEY)
        revised_payload = merge_dict(payload, public_key_dict)
        return cls.create(account_endpoint, api, revised_payload)


class Transaction(Create, List):
    @classmethod
    def verify(cls, payload, api):
        endpoint = '/flwv3-pug/getpaidx/api/verify'
        secret_key_dict = dict(SECKEY=api.SECRET_KEY)
        updated_valid_payload = merge_dict(payload, secret_key_dict)
        return cls.create(endpoint, api, updated_valid_payload)

    @classmethod
    def verify_xquery(cls, payload, api):
        endpoint = '/flwv3-pug/getpaidx/api/xrequery'
        secret_key_dict = dict(SECKEY=api.SECRET_KEY)
        updated_valid_payload = merge_dict(payload, secret_key_dict)
        return cls.create(endpoint, api, updated_valid_payload)

    @classmethod
    def list_all(cls, api):
        endpoint = '/merchant/subscriptions/list'
        params = dict(seckey=api.SECRET_KEY)
        return cls.list(endpoint, api, params)

    @classmethod
    def list_single(cls, params, api):
        endpoint = '/merchant/subscriptions/list'
        params = dict(seckey=api.SECRET_KEY, txId=params)
        return cls.list(endpoint, api, params)


class Refund(Create):
    @classmethod
    def create_refund(cls, payload, api):
        endpoint = '/gpx/merchant/transactions/refund'
        secret_key_dict = dict(SECKEY=api.SECRET_KEY)
        updated_valid_payload = merge_dict(payload, secret_key_dict)
        return cls.create(endpoint, api, updated_valid_payload)
