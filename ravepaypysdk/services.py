from resources import Create, List
from utils.rave_utils import merge_dict, initialize_config


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
        secret_key_dict = dict(SECKEY=api.SECRET_KEY)
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
        secret_key_dict = dict(SECKEY=api.SECRET_KEY)
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
        :param payload:
        :param api:
        :return:
        """
        endpoint = '/flwv3-pug/getpaidx/api/validatecharge'
        public_key_dict = dict(PBFPubKey=api.PUBLIC_KEY)
        revised_payload = merge_dict(payload, public_key_dict)
        request = cls.create(endpoint, api, revised_payload)
        return request

    @classmethod
    def account(cls, payload, api):
        """
        Validate direct charge payments made with bank account
        """
        account_endpoint = '/flwv3-pug/getpaidx/api/validate'
        public_key_dict = dict(PBFPubKey=api.PUBLIC_KEY)
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
        secret_key_dict = dict(SECKEY=api.SECRET_KEY)
        updated_valid_payload = merge_dict(payload, secret_key_dict)
        return cls.create(endpoint, api, updated_valid_payload)

    @classmethod
    def verify_query(cls, payload, api):
        """
        Verifies a user's transaction with xrequery
        """
        endpoint = '/flwv3-pug/getpaidx/api/xrequery'
        secret_key_dict = dict(SECKEY=api.SECRET_KEY)
        updated_valid_payload = merge_dict(payload, secret_key_dict)
        return cls.create(endpoint, api, updated_valid_payload)

    @classmethod
    def list_all_recurring(cls, api):
        """
        Gets all recurring transactions
        """
        endpoint = '/merchant/subscriptions/list'
        params = dict(seckey=api.SECRET_KEY)
        return cls.list(endpoint, api, params)

    @classmethod
    def list_single_recurring(cls, params, api):
        """
        Gets a single recurring transaction
        """
        endpoint = '/merchant/subscriptions/list'
        params = dict(seckey=api.SECRET_KEY, txId=params)
        return cls.list(endpoint, api, params)

    @classmethod
    def refund(cls, payload, api):
        """
        Process getting refunds after transaction
        """
        endpoint = '/gpx/merchant/transactions/refund'
        secret_key_dict = dict(SECKEY=api.SECRET_KEY)
        updated_valid_payload = merge_dict(payload, secret_key_dict)
        return cls.create(endpoint, api, updated_valid_payload)

    @classmethod
    def stop_recurring_payment(cls, payload, api):
        """
        processes stop recurring payment transacyions
        """
        endpoint = "/merchant/subscriptions/stop"
        secret_key_dict = dict(seckey=api.SECRET_KEY)
        id = payload.get('id')
        if not id:
            return KeyError('Id field is required for this transaction')
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
        secret_key_dict = dict(SECKEY=api.SECRET_KEY)
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
            raise KeyError('Card number and CVV are required for card transactions. Kindly check your payload')
        else:
            card_payload = initialize_config(payload, api)
            return cls.create(cls.endpoint, api, card_payload)

    @classmethod
    def account(cls, payload, api):
        """
        Process payment from bank accounts (Only available in Nigeria)
        """
        account_number = payload.get('accountnumber')
        account_bank = payload.get('accountbank')
        if not (account_bank and account_number):
            raise KeyError(
                'Account number and bank are required fields for this transaction. Kindly check the documentation')
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
            raise KeyError('Ghana mobile money fields are required for this transaction')
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
            raise KeyError('USSD fields are required for this transaction. Check your payload')
        else:
            ussd_payload = initialize_config(payload, api)
            return cls.create(cls.endpoint, api, ussd_payload)

    @classmethod
    def tokenize_card(cls, payload, api):
        """
        This function allows users let their card be charged with tokens
        """
        endpoint = 'flwv3-pug/getpaidx/api/tokenized/charge'
        secret_key_dict = dict(SECKEY=api.SECRET_KEY)
        email = payload.get('email')
        token_payload = merge_dict(secret_key_dict, payload)
        if not email:
            raise KeyError('You need to pass the same email used in the initial charge')
        return cls.create(endpoint, api, token_payload)
