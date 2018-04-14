"""
This module handles all the REST Services for RavePay
"""

from .helpers import Create, List
from .utils.rave_utils import merge_dict, initialize_config


class PreAuthorization(Create):
    """
    Preauthorization for refunds and card transactions
    """

    @classmethod
    def capture(cls, payload, api):
        """
        process preauthorization of capture transactions

        """
        endpoint = '/flwv3-pug/getpaidx/api/capture'
        secret_key_dict = dict(SECKEY=api.secret_key)
        capture_payload = merge_dict(payload, secret_key_dict)
        if capture_payload:
            return cls.create(endpoint, api, capture_payload)

    @classmethod
    def preauthorize_card(cls, payload, api):
        """
        process preauthorization of cards before transactions
        """
        endpoint = '/flwv3-pug/getpaidx/api/charge'
        preauthorize_payload = initialize_config(payload, api)
        if preauthorize_payload:
            return cls.create(endpoint, api, preauthorize_payload)

    @classmethod
    def void_or_refund(cls, payload, api):
        """
        processes preauthorization of refunds and void transactions
        """
        endpoint = '/flwv3-pug/getpaidx/api/refundorvoid'
        secret_key_dict = dict(SECKEY=api.secret_key)
        updated_void_payload = merge_dict(secret_key_dict, payload)
        return cls.create(endpoint, api, updated_void_payload)


class ValidateCharge(Create):
    """
    Validates Payment transactions for RavePay
    """

    @classmethod
    def card(cls, payload, api):
        """
        Validate direct charge payments made with card
        """
        endpoint = '/flwv3-pug/getpaidx/api/validatecharge'
        public_key_dict = dict(PBFPubKey=api.public_key)
        revised_payload = merge_dict(payload, public_key_dict)
        request = cls.create(endpoint, api, revised_payload)
        return request

    @classmethod
    def account(cls, payload, api):
        """
        Validate direct charge payments made with bank account
        """
        account_endpoint = '/flwv3-pug/getpaidx/api/validate'
        public_key_dict = dict(PBFPubKey=api.public_key)
        revised_payload = merge_dict(payload, public_key_dict)
        return cls.create(account_endpoint, api, revised_payload)


class Transaction(Create, List):
    """
    Process Transactions with RavePay API
    """

    @classmethod
    def verify(cls, payload, api):
        """
        Verifies a user's transaction

        """
        endpoint = '/flwv3-pug/getpaidx/api/verify'
        secret_key_dict = dict(SECKEY=api.secret_key)
        updated_valid_payload = merge_dict(payload, secret_key_dict)
        return cls.create(endpoint, api, updated_valid_payload)

    @classmethod
    def verify_query(cls, payload, api):
        """
        Verifies a user's transaction with xrequery
        """
        endpoint = '/flwv3-pug/getpaidx/api/xrequery'
        secret_key_dict = dict(SECKEY=api.secret_key)
        updated_valid_payload = merge_dict(payload, secret_key_dict)
        return cls.create(endpoint, api, updated_valid_payload)

    @classmethod
    def list_all_recurring(cls, api):
        """
        Gets all recurring transactions
        """
        endpoint = '/merchant/subscriptions/list'
        params = dict(seckey=api.secret_key)
        return cls.list(endpoint, api, params)

    @classmethod
    def list_single_recurring(cls, payload, api):
        """
        Gets a single recurring transaction
        """
        tx_id = payload.get('txId')
        endpoint = '/merchant/subscriptions/list'
        params = dict(seckey=api.secret_key, txId=tx_id)
        return cls.list(endpoint, api, params)

    @classmethod
    def refund(cls, payload, api):
        """
        Process getting refunds after transaction
        """
        endpoint = '/gpx/merchant/transactions/refund'
        secret_key_dict = dict(SECKEY=api.secret_key)
        updated_valid_payload = merge_dict(payload, secret_key_dict)
        return cls.create(endpoint, api, updated_valid_payload)

    @classmethod
    def stop_recurring_payment(cls, payload, api):
        """
        processes stop recurring payment transacyions
        """
        endpoint = "/merchant/subscriptions/stop"
        secret_key_dict = dict(seckey=api.secret_key)
        merchant_id = payload.get('id')
        if not merchant_id:
            raise KeyError('Id field is required for this transaction')
        else:
            updated_payload = merge_dict(secret_key_dict, payload)
            return cls.create(endpoint, api, updated_payload)


class Bank(Create, List):
    """
    Class for processing bank related information
    """

    @classmethod
    def list_all(cls, api):
        """
        Get all banks in Nigeria compatible with rave pay
        """
        endpoint = '/flwv3-pug/getpaidx/api/flwpbf-banks.js?json=1'
        return cls.list(endpoint, api)

    @classmethod
    def get_forex(cls, payload, api):
        """
        Get current forex exchange rates
        """
        secret_key_dict = dict(SECKEY=api.secret_key)
        updated_valid_payload = merge_dict(payload, secret_key_dict)
        endpoint = '/flwv3-pug/getpaidx/api/forex'
        return cls.create(endpoint, api, updated_valid_payload)


class Payment(Create):
    """
    Class for processing rave direct charge payments
    """
    endpoint = '/flwv3-pug/getpaidx/api/charge'

    @classmethod
    def card(cls, payload, api):
        """
        Process direct charge payment from cards
        """
        if not (payload.get('cardno') and payload.get('cvv')):
            raise KeyError('Card number and CVV are  \
            required for card transactions. Kindly check your payload')
        else:
            card_payload = initialize_config(payload, api)
            return cls.create(cls.endpoint, api, card_payload)

    @classmethod
    def bank_account(cls, payload, api):
        """
        Process payment from bank accounts (Only available in Nigeria)
        """
        account_number = payload.get('accountnumber')
        account_bank = payload.get('accountbank')
        if not (account_bank and account_number):
            raise KeyError(
                'Account number and bank are required fields \
                 for this transaction.Kindly check the documentation')
        else:
            account_payload = initialize_config(payload, api)
            return cls.create(cls.endpoint, api, account_payload)

    @classmethod
    def mpesa(cls, payload, api):
        """
        Processes mpesa money payment
        """
        is_mpesa = payload.get('is_mpesa')
        payment_type = payload.get('payment-type')
        if not (is_mpesa and payment_type == 'mpesa'):
            raise KeyError('Mpesa money fields are required for this transaction')
        else:
            mpesa_payload = initialize_config(payload, api)
            return cls.create(cls.endpoint, api, mpesa_payload)

    @classmethod
    def ghana_mobile(cls, payload, api):
        """
        Processes Ghana mobile money payment
        """
        gh_mobile = payload.get('is_mobile_money_gh')
        payment_type = payload.get('payment-type')
        if not (gh_mobile and payment_type == 'mobilemoneygh'):
            raise KeyError('Ghana mobile money fields are required \
             for this transaction')
        else:
            gh_mobile_money_payload = initialize_config(payload, api)
            return cls.create(cls.endpoint, api, gh_mobile_money_payload)

    @classmethod
    def ussd(cls, payload, api):
        """
        Process USSD payment
        """
        is_ussd = payload.get('is_ussd')
        payment_type = payload.get('payment_type')
        if not (is_ussd and payment_type == 'ussd'):
            raise KeyError('USSD fields are required for this transaction.\
             Check your payload')
        else:
            ussd_payload = initialize_config(payload, api)
            return cls.create(cls.endpoint, api, ussd_payload)

    @classmethod
    def tokenize_card(cls, payload, api):
        """
        This function allows users let their card be charged with tokens
        """
        endpoint = 'flwv3-pug/getpaidx/api/tokenized/charge'
        secret_key_dict = dict(SECKEY=api.secret_key)
        email = payload.get('email')
        token_payload = merge_dict(secret_key_dict, payload)
        if not email:
            raise KeyError('You need to pass the same email \
             used in the initial charge')
        return cls.create(endpoint, api, token_payload)


class PaymentPlan(Create, List):
    """
     Class for processing payment plan on the ravepay platform
     """

    @classmethod
    def create_plan(cls, payload, api):
        endpoint = 'v2/gpx/paymentplans/create'
        secret_key_dict = dict(seckey=api.secret_key)
        plan_payload = merge_dict(payload, secret_key_dict)
        return cls.create(endpoint, api, plan_payload)

    @classmethod
    def fetch_all_plan(cls, api):
        endpoint = 'v2/gpx/paymentplans/query'
        secret_key_dict = dict(seckey=api.secret_key)
        return cls.list(endpoint, api, secret_key_dict)

    @classmethod
    def fetch_single_plan(cls, params, api):
        endpoint = 'v2/gpx/paymentplans/query'
        secret_key_dict = dict(seckey=api.secret_key)
        fetch_params = merge_dict(params, secret_key_dict)
        return cls.list(endpoint, api, fetch_params)

    @classmethod
    def cancel_plan(cls, plan_id=None, api=None):
        if plan_id is not None:
            endpoint = 'v2/gpx/paymentplans/{}/cancel'.format(plan_id)
            secret_key_dict = dict(seckey=api.secret_key)
            return cls.create(endpoint, api, secret_key_dict)
        return None

    @classmethod
    def edit_plan(cls, payload=None, plan_id=None, api=None):
        if plan_id is not None:
            endpoint = 'v2/gpx/paymentplans/{}/edit'.format(plan_id)
            secret_key_dict = dict(seckey=api.secret_key)
            if payload is not None:
                edit_payload = merge_dict(payload, secret_key_dict)
                return cls.create(endpoint, api, edit_payload)
            return cls.create(endpoint, api, secret_key_dict)


class Subscriptions(Create, List):
    @classmethod
    def fetch_all(cls, api):
        endpoint = 'v2/gpx/subscriptions/query'
        secret_key_dict = dict(seckey=api.secret_key)
        return cls.list(endpoint, api, secret_key_dict)

    @classmethod
    def fetch_single(cls, params=None, api=None):
        endpoint = 'v2/gpx/subscriptions/query'
        if params is not None:
            secret_key = dict(seckey=api.secret_key)
            fetch_params_dict = merge_dict(params, secret_key)
            return cls.list(endpoint, api, fetch_params_dict)
        return None

    @classmethod
    def cancel(cls, sub_id=None, api=None):
        if sub_id is not None:
            endpoint = 'v2/gpx/subscriptions/{}/cancel'.format(sub_id)
            secret_key = dict(seckey=api.secret_key)
            return cls.create(endpoint, api, secret_key)
        return None

    @classmethod
    def activate(cls, sub_id=None, api=None):
        if sub_id is not None:
            endpoint = 'v2/gpx/subscriptions/{}/activate'.format(sub_id)
            secret_key = dict(seckey=api.secret_key)
            return cls.create(endpoint, api, secret_key)
        return None
