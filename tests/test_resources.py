import os
import unittest
from unittest.mock import patch
from dotenv import load_dotenv, find_dotenv
from ravepaypysdk.api import Api
from ravepaypysdk.resources import Transaction, Payment, Bank, PreAuthorization, ValidateCharge

load_dotenv(find_dotenv())


class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.new_api = Api(
            secret_key='dummy',
            public_key='dummy',
            production=False
        )
        self.payload = dict(error=False, Payment=1200, id=2)

    @patch('ravepaypysdk.resources.List.list')
    def test_single_recurring_transaction(self, mock):
        self.single_recurring_transac_payload = {
            "txId": 1
        }
        mc = mock.return_value
        mc.list.return_value = True
        result = Transaction.list_single_recurring(self.single_recurring_transac_payload, api=self.new_api)
        mock.assert_called_once_with('/merchant/subscriptions/list', self.new_api, {'seckey': 'dummy', 'txId': 1})
        self.assertTrue(result)

    @patch('ravepaypysdk.resources.List.list')
    def test_list_all_recurring_transaction(self, mock):
        mc = mock.return_value
        mc.list.return_value = True
        response = Transaction.list_all_recurring(api=self.new_api)
        mock.assert_called_once_with('/merchant/subscriptions/list', self.new_api, {'seckey': 'dummy'})
        self.assertTrue(response)

    @patch('ravepaypysdk.resources.Create.create')
    def test_refund(self, mock):
        mc = mock.return_value
        mc.list.return_value = True
        response = Transaction.refund(self.payload, api=self.new_api)
        mock.assert_called_once_with('/gpx/merchant/transactions/refund', self.new_api,
                                     {'error': False, 'Payment': 1200, 'id': 2, 'SECKEY': 'dummy'})
        self.assertTrue(response)

    @patch('ravepaypysdk.resources.Create.create')
    def test_stop_recurring_payment(self, mock):
        mc = mock.return_value
        mc.return_value = True
        response = Transaction.stop_recurring_payment(self.payload, api=self.new_api)
        mock.assert_called_once_with("/merchant/subscriptions/stop", self.new_api,
                                     {'seckey': 'dummy', 'error': False, 'Payment': 1200, 'id': 2})
        self.assertTrue(response)

    @patch('ravepaypysdk.resources.Create.create')
    def test_verify_transaction(self, mock):
        path = '/flwv3-pug/getpaidx/api/verify'
        mc = mock.return_value
        mc.return_value = True
        verify_response = Transaction.verify(self.payload, api=self.new_api)
        mock.assert_called_once_with(path, self.new_api, {
            'error': False, 'Payment': 1200, 'id': 2, 'SECKEY': 'dummy'})
        self.assertTrue(verify_response)

    @patch('ravepaypysdk.resources.Create.create')
    def test_xquery_verify_transaction(self, mock):
        path = '/flwv3-pug/getpaidx/api/xrequery'
        xquery_response = Transaction.verify_query(self.payload, api=self.new_api)
        mock.assert_called_once_with(
            path, self.new_api, {
                'error': False, 'Payment': 1200, 'id': 2, 'SECKEY': 'dummy'}
        )
        self.assertTrue(xquery_response)


class TestPayment(unittest.TestCase):
    def setUp(self):
        self.new_api = Api(
            secret_key=os.environ.get('secret_key'),
            public_key='dummy',
            production=False
        )
        self.path = '/flwv3-pug/getpaidx/api/charge'
        self.card_payload = dict(error=False, cardno='34343', cvv='232', email='jb@gmail.com')
        self.bank_payload = dict(error=False, accountnumber='34343', accountbank='232')
        self.mpesa_payload = {
            'payment-type': 'mpesa',
            'is_mpesa': 1
        }
        self.gh_mobile_payload = {
            'payment-type': 'mobilemoneygh',
            'is_mobile_money_gh': 1
        }
        self.ussd_payload = {
            'payment_type': 'ussd',
            'is_ussd': 1
        }

    @patch('ravepaypysdk.resources.Create.create')
    def test_card_direct_payment(self, mock):
        Payment.card(self.card_payload, api=self.new_api)
        mock.assert_called_once_with(self.path, self.new_api,
                                     {
                                         'client': b'Zah+qD4JviOdUFttZL7d0MgB/LPtEW4Gz7werMMDtOIWZLCGeZ7hRb0PlZbPU6JfELIgpyUP/L9ylb58B6EpXGPYHhYjC/Uza94nb4ZLiJM=',
                                         'PBFPubKey': 'dummy', 'alg': '3DES-24'})

    @patch('ravepaypysdk.resources.Create.create')
    def test_bank_account_direct_payment(self, mock):
        Payment.bank_account(self.bank_payload, api=self.new_api)
        mock.assert_called_once_with(self.path, self.new_api,
                                     {
                                         'client': b'Zah+qD4JviOdUFttZL7d0D1iXdxyTXxBCbWZvXCfmUrkhNr7MxySJLe/01oZZxph27HEjbbOZVJCsD+WMA8Cjj78w8CcOF0t',
                                         'PBFPubKey': 'dummy', 'alg': '3DES-24'})

    @patch('ravepaypysdk.resources.Create.create')
    def test_mpesa_direct_payment(self, mock):
        Payment.mpesa(self.mpesa_payload, self.new_api)
        mock.assert_called_once_with(self.path, self.new_api,
                                     {
                                         'client': b'BX1KArxf7xAngqqNs/uWpMcxilwH0CmJ0pMwxLLFPtXClSO3y4oSqD78w8CcOF0t',
                                         'PBFPubKey': 'dummy', 'alg': '3DES-24'})

    @patch('ravepaypysdk.resources.Create.create')
    def test_gh_money_payment(self, mock):
        Payment.ghana_mobile(self.gh_mobile_payload, self.new_api)
        mock.assert_called_once_with(self.path, self.new_api,
                                     {
                                         'client': b'BX1KArxf7xAngqqNs/uWpF1xwWg3A0stKlGYVIidO/hNNG86I+JiSE7q7FFVlKolnQv3RdAjAqQu0ZCzmKFRog==',
                                         'PBFPubKey': 'dummy', 'alg': '3DES-24'})

    @patch('ravepaypysdk.resources.Create.create')
    def test_ussd_payment(self, mock):
        Payment.ussd(self.ussd_payload, self.new_api)
        mock.assert_called_once_with(self.path, self.new_api,
                                     {
                                         'client': b'BX1KArxf7xCQvJirHHQBNK1AAZ9qzlza9vNv8GjMkIqsM6leOIFazg==',
                                         'PBFPubKey': 'dummy', 'alg': '3DES-24'})

    @patch('ravepaypysdk.resources.Create.create')
    def test_tokenize_card(self, mock):
        path = 'flwv3-pug/getpaidx/api/tokenized/charge'
        Payment.tokenize_card(self.card_payload, self.new_api)
        mock.assert_called_once_with(path, self.new_api,
                                     {'SECKEY': 'FLWSECK-cc8399cf35c2d1cfb62dd44c3c13f9ab-X', 'error': False,
                                      'cardno': '34343', 'cvv': '232', 'email': 'jb@gmail.com'})


class TestBank(unittest.TestCase):
    def setUp(self):
        self.api = Api(
            secret_key=os.environ.get('secret_key'),
            public_key='dummy',
            production=False
        )

    @patch('ravepaypysdk.resources.List.list')
    def test_get_all_banks(self, mock):
        path = '/flwv3-pug/getpaidx/api/flwpbf-banks.js?json=1'

        Bank.list_all(api=self.api)
        mock.assert_called_once_with(path, self.api)

    @patch('ravepaypysdk.resources.Create.create')
    def test_get_forex(self, mock):
        path = '/flwv3-pug/getpaidx/api/forex'
        payload = {
            'origin_currency': 'USD',
            'destination_currency': 'NGN',
            'amount': '200'
        }
        Bank.get_forex(payload, api=self.api)
        mock.assert_called_once_with(
            path, self.api, {
                'origin_currency': 'USD', 'destination_currency': 'NGN', 'amount': '200',
                'SECKEY': 'FLWSECK-cc8399cf35c2d1cfb62dd44c3c13f9ab-X'}
        )


class TestPreauthorization(unittest.TestCase):
    def setUp(self):
        self.api = Api(
            secret_key=os.environ.get('secret_key'),
            public_key='dummy',
            production=False
        )

    @patch('ravepaypysdk.resources.Create.create')
    def test_preauthorize_card(self, mock):
        path = '/flwv3-pug/getpaidx/api/charge'
        payload = dict(error=False, cardno='34343', cvv='232', email='jb@gmail.com')

        PreAuthorization.preauthorize_card(payload, api=self.api)
        mock.assert_called_once_with(
            path, self.api, {
                'client': b'Zah+qD4JviOdUFttZL7d0MgB/LPtEW4Gz7werMMDtOIWZLCGeZ7hRb0PlZbPU6JfELIgpyUP/L9ylb58B6EpXGPYHhYjC/Uza94nb4ZLiJM=',
                'PBFPubKey': 'dummy', 'alg': '3DES-24'}
        )

    @patch('ravepaypysdk.resources.Create.create')
    def test_capture(self, mock_capture):
        path = '/flwv3-pug/getpaidx/api/capture'
        payload = dict(error=False, email='jb@gmail.com')

        PreAuthorization.capture(payload, api=self.api)
        mock_capture.assert_called_once_with(
            path, self.api, {
                'error': False, 'email': 'jb@gmail.com',
                'SECKEY': 'FLWSECK-cc8399cf35c2d1cfb62dd44c3c13f9ab-X'}
        )

    @patch('ravepaypysdk.resources.Create.create')
    def test_void_refund(self, mock):
        path = '/flwv3-pug/getpaidx/api/refundorvoid'
        payload = dict(error=False, email='jb@gmail.com')

        PreAuthorization.void_or_refund(payload, api=self.api)
        mock.assert_called_once_with(
            path, self.api,
            {'error': False, 'email': 'jb@gmail.com', 'SECKEY': 'FLWSECK-cc8399cf35c2d1cfb62dd44c3c13f9ab-X'}
        )


class TestValidateCharge(unittest.TestCase):
    def setUp(self):
        self.api = Api(
            secret_key=os.environ.get('secret_key'),
            public_key='dummy',
            production=False
        )
        self.payload = dict(error=False, cardno='34343', cvv='232', email='jb@gmail.com')
        self.card_path = '/flwv3-pug/getpaidx/api/validatecharge'
        self.account_path = '/flwv3-pug/getpaidx/api/validate'

    @patch('ravepaypysdk.resources.Create.create')
    def test_card_validation(self, mock):
        ValidateCharge.card(self.payload, api=self.api)
        mock.assert_called_once_with(
            self.card_path, self.api, {
                'error': False, 'cardno': '34343', 'cvv': '232',
                'email': 'jb@gmail.com', 'PBFPubKey': 'dummy'}
        )

    @patch('ravepaypysdk.resources.Create.create')
    def test_account_validation(self, mock):
        ValidateCharge.account(self.payload, api=self.api)
        mock.assert_called_once_with(
            self.account_path, self.api, {
                'error': False, 'cardno': '34343', 'cvv': '232',
                'email': 'jb@gmail.com', 'PBFPubKey': 'dummy'}
        )
