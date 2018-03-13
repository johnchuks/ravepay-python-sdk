import os
import unittest
from unittest.mock import patch

from dotenv import load_dotenv, find_dotenv

from ravepaypysdk.api import Api
from ravepaypysdk.services import Transaction, Payment

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
        self.txId = 1
        mc = mock.return_value
        mc.list.return_value = True
        result = Transaction.list_single_recurring(self.txId, api=self.new_api)
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


class TestPayment(unittest.TestCase):
    def setUp(self):
        self.new_api = Api(
            secret_key=os.environ.get('SECRET_KEY'),
            public_key='dummy',
            production=False
        )
        self.path = '/flwv3-pug/getpaidx/api/charge'
        self.card_payload = dict(error=False,cardno='34343', cvv='232', email='jb@gmail.com')
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
                                         'client':b'Zah+qD4JviOdUFttZL7d0MgB/LPtEW4Gz7werMMDtOIWZLCGeZ7hRb0PlZbPU6JfELIgpyUP/L9ylb58B6EpXGPYHhYjC/Uza94nb4ZLiJM=',
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
        path ='flwv3-pug/getpaidx/api/tokenized/charge'
        Payment.tokenize_card(self.card_payload, self.new_api)
        mock.assert_called_once_with(path, self.new_api,
                                     {'SECKEY': 'FLWSECK-cc8399cf35c2d1cfb62dd44c3c13f9ab-X', 'error': False,
                                      'cardno': '34343', 'cvv': '232', 'email': 'jb@gmail.com'})

class TestBank(unittest.TestCase):
    pass
