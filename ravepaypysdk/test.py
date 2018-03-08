import requests
import os
import json
from dotenv import find_dotenv, load_dotenv
from utils.encryption import encrypt_data
from api import Api
from services import RaveDirectCharge, ValidateCardCharge

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
stringified_data = json.dumps(client_payload)
encrypted_data = encrypt_data(stringified_data)
payload = dict(PBFPubKey=os.environ.get('PUBLIC_KEY'), client=encrypted_data, alg='3DES-24')
validate_payload = dict(transaction_reference='FLW-MOCK-3b2b32a21032b5a0099faf993a416cad', otp='12345')

new_api = Api(
    secret_key=os.environ.get('SECRET_KEY'),
    public_key=os.environ.get('PUBLIC_KEY'),
    production=False
)

# payment = RaveDirectCharge.create(payload, api=new_api)
direct_charge = RaveDirectCharge()

validation = ValidateCardCharge.post(validate_payload, api=new_api)

print(validation, '----->>>>')
# new_pay = RaveDirectCharge.create_payment(payload, api=new_api)
# #
# print(new_pay, '-----------')
#
# response = requests.request("POST", url, data=payload)
#
# print(response.text)