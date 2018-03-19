import os
import unittest
import json
from unittest.mock import Mock, patch

from dotenv import find_dotenv, load_dotenv

from ravepaypysdk.api import Api

load_dotenv(find_dotenv())


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.api = Api(
            secret_key=os.environ.get('secret_key'),
            public_key=os.environ.get('public_key'),
            production=False
        )
        self.new_api = Api()
        self.account_attributes = {
            "accountnumber": "0690000031",
            "accountbank": "044",
            "currency": "NGN",
            "country": "NG",
            "amount": "10",
            "email": "johnb@gmail.com",
            "phonenumber": "07088691390",
            "firstname": "johnb",
            "lastname": "chuks",
            "IP": "355426087298442",
            "txRef": "",
            "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
        }

        self.gh_money_payload = {
            "cardno": "5438898014560229",
            "cvv": "789",
            "is_mobile_money_gh": "1",
            "payment-type": "mobilemoneygh",
            "expirymonth": "07",
            "expiryyear": "18",
            "currency": "NGN",
            "pin": "7552",
            "country": "GH",
            "amount": "10",
            "email": "user@example.com",
            "phonenumber": "1234555",
            "suggested_auth": "PIN",
            "firstname": "user1",
            "lastname": "user2",
            "IP": "355426087298442",
            "txRef": "MC-7663-YU",
            "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
        }

        self.api.request = Mock()

    def test_ravepay_config(self):
        self.api_dev = Api(
            public_key='dummy',
            secret_key='dummy',
            production=False
        )
        self.api_live = Api(
            public_key='dummy',
            secret_key='dummy',
            production=True
        )
        self.assertEqual(self.api_dev.url, 'http://flw-pms-dev.eu-west-1.elasticbeanstalk.com')
        self.assertEqual(self.api_live.url, 'https://api.ravepay.co')
        self.assertEqual(self.api_dev.secret_key, 'dummy')
        self.assertEqual(self.api_dev.public_key, 'dummy')

    def test_get(self):
        params_test = dict(SECKEY=os.environ.get('secret_key'))
        endpoint = '/merchant/subscriptions/list'

        self.api.get(endpoint, params_test)
        self.api.request.assert_called_once_with('GET',
                                                 'http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/merchant/subscriptions/list',
                                                 params=params_test, payload=None
                                                 )

    def test_post(self):
        endpoint = '/flwv3-pug/getpaidx/api/verify'
        payload = {'name': 'johnbosco', 'occupation': 'we there', 'SECKEY': os.environ.get('SECKEY')}

        self.api.post(endpoint, payload)
        self.api.request.assert_called_once_with(
            'POST', 'http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/flwv3-pug/getpaidx/api/verify', payload=payload
        )

    def test_put(self):
        endpoint = '/flwv3-pug/getpaidx/api/verify'
        params = dict(SECKEY=os.environ.get('secret_key'))
        self.api.put(endpoint, payload=self.account_attributes, query_string=params)

        self.api.request.assert_called_once_with(
            'PUT', 'http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/flwv3-pug/getpaidx/api/verify', params=params,
            payload=self.account_attributes,
        )

    def test_bad_request(self):
        self.api.request.return_value = {"status": "error", "message": "USSD charges can only be done in Ghana Cedis",
                                         "data": {"code": "ERR",
                                                  "message": "USSD charges can only be done in Ghana Cedis"}}
        gh_money_charge = self.api.post('/flwv3-pug/getpaidx/api/charge', self.gh_money_payload)
        self.api.request.assert_called_once_with(
            'POST', "http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/flwv3-pug/getpaidx/api/charge",
            payload=self.gh_money_payload
        )
        self.assertEqual(gh_money_charge.get('status'), 'error')

    @patch('ravepaypysdk.api.requests.get')
    def test_request_get(self, mock):
        mock.return_value.status_code = 200
        mock.return_value.text =  dict(error=False,cardno='34343', cvv='232', email='jb@gmail.com')
        path = 'http://jsonplaceholder.typicode.com/posts'
        params = dict(userId=1)
        response = self.new_api.request('GET', path, params=params)
        self.assertEqual(response['status_code'], 200)

    @patch('ravepaypysdk.api.requests.post')
    def test_request_post(self, mock):
        mock.return_value.status_code = 201
        payload = json.dumps(dict(title='rave api', body='sdk for rave', userId=1))
        path = 'http://jsonplaceholder.typicode.com/posts'

        response = self.new_api.request('POST', path, payload=payload)

        self.assertEqual(response['status_code'], 201)

    @patch('ravepaypysdk.api.requests.get')
    def test_request_get_without_params(self, mock):
        mock.return_value.status_code = 200
        path = 'http://jsonplaceholder.typicode.com/posts'

        response = self.new_api.request('GET', path)

        self.assertEqual(response['status_code'], 200)






