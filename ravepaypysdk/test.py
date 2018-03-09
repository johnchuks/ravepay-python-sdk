import requests
import os
import json
from dotenv import find_dotenv, load_dotenv
from utils.encryption import encrypt_data
from api import Api
from services import Card, ValidateCharge, Transaction, Bank

url = "http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/flwv3-pug/getpaidx/api/charge"

client_payload = {
    "cardno": "5438898014560229",
    "cvv": "789",
    "expirymonth": "07",
    "expiryyear": "18",
    "currency": "NGN",
    "pin": "7552",
    "country": "NG",
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

# payload = dict(client=client_payload, alg='3DES-24')
# validate_payload = dict(transaction_reference='FLW-MOCK-bad59ea46faf0f0e9935826893c3070b', otp='12345')
#
new_api = Api(secret_key=os.environ.get('SECRET_KEY'),
              public_key=os.environ.get('PUBLIC_KEY'),
              production=False)
#
# payment = Card.preauth_card(client_payload, api=new_api)
# # direct_charge = RaveDirectCharge()
# print(payment, 'payment')
# validation = ValidateCharge.card(validate_payload, api=new_api)
#
# print(validation, '----->>>>')

# transactions = Transaction.list_one(tx_id=api=new_api)
#
# print(transactions)
# new_pay = RaveDirectCharge.create_payment(payload, api=new_api)
#
# print(new_pay, '-----------')
payload = {
    'origin_currency': 'USD',
    'destination_currency': 'NGN',
    'amount': '200'
}
bank = Bank.get_forex(payload, api=new_api)
print(bank, '------')
