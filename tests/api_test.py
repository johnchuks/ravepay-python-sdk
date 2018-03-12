import ravepaypysdk
import os
from dotenv import find_dotenv, load_dotenv
import unittest
from unittest import mock

load_dotenv(find_dotenv())


class ApiTest(unittest.TestCase):

    def setUp(self):
        self.api = Api(
            secret_key=os.environ.get('SECRET_KEY'),
            public_key=os.environ.get('PUBLIC_KEY'),
            production=False
        )
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

    def test_ravepay_base_url(self):
        self.api_dev = Api(
            public_key='dummy',
            secret_key='dummy',
            production=False
        )
        self.assertEqual(self.api_dev.url, 'http://flw-pms-dev.eu-west-1.elasticbeanstalk.com')
