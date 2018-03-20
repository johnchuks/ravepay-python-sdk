# RavePay-SDK-Python
[![Build Status](https://travis-ci.org/johnchuks/RavePay-SDK-Python.svg?branch=master)](https://travis-ci.org/johnchuks/RavePay-SDK-Python)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/johnchuks/RavePay-SDK-Python/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/johnchuks/RavePay-SDK-Python/?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/johnchuks/RavePay-SDK-Python/badge.svg?branch=master)](https://coveralls.io/github/johnchuks/RavePay-SDK-Python?branch=master)

The RavePay Python SDK provides APIs to create, process and manage payments on the RavePay platform. The SDK fully supports the API

## Installation
`pip install ravepaypysdk`

## Configuring RavePay SDK
```
import ravepaypysdk

my_api = ravepaypysdk.Api(
          secret_key='ravepay_secret_key'
          public_key='ravepay_public_key'
          production=False # sandbox # or True # Live
        )
```

## Usage
To start using the SDK ensure you have your public key and secret key instantiated with the `Api` object 

## Payments (RavePay Direct Charge)
  Import the RavePay Payment module
  ```
  from ravepaypysdk import Payment
  ```
  There are 5 different ways to utilize RavePay's direct charge for payment:

  - **Card direct charge**

      *Usage*
      ```
      payload = {
          "cardno": "5438898014560229",
          "cvv": "789",
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
      card_payment = Payment.card(payload, api=my_api)

      if card_payment:
        return card_payment
      ```
      The `payload` object should client data as show above 

  -  **Bank account payment**
     
     *Usage*
     ```
     payload = {
       "accountnumber": "0690000004",
       "accountbank": "044",
       "currency": "NGN",
       "country": "NG",
       "amount": "10",
       "email": "user@example.com",
       "phonenumber": "1234555",
       "firstname": "first name",
       "lastname": "last name",
       "IP": "355426087298442",
       "txRef": "",
       "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
     }
     bank_payment = Payment.bank_account(payload, api=my_api)

     if bank_payment:
        return bank_payment

        ```
  -  **Tokenize Card**

     *Usage*
     ```
     payload = {
       "token":{
           “chargeToken”:{
                “user_token”:“f0209”,
                “embed_token”:“flw-t0-9f3aa69a806f6440fbb78cc9e8b2f135-k3n”
            }
       },
       "currency": "NGN",
       "country": "NG",
       "amount": "10",
       "email": "user@example.com",
       "phonenumber": "1234555",
       "firstname": "user1",
       "lastname": "user2",
       "IP": "355426087298442",
       "txRef": "MC-7663-YU",
       "narration":"tokenize my card"
       "meta": [{"metaname": "flightId"}, {"metavalue": "1002"}]
       "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
     }

     tokenize_card = Payment.tokenize_card(payload, api=my_api)
     ```
  -  **USSD Payment**

     *Usage*
     ```
     ussd_payment = Payment.ussd(payload, api=my_api)
     ```

  -  **MPESA Payment**

     *Usage*
     ```
     mpesa_payment = Payment.mpesa(payload, api=my_api)
     ```

  -  **Ghana Mobile Money**

     *Usage*
     ```
     gh_mobile_payment = Payment.ghana_mobile(payloadm api=my_api)
     ```

  - The same payload format goes for the **USSD**, **MPESA** and **Ghana Mobile Money**. Kindly review the [API documentation](https://flutterwavedevelopers.readme.io/v1.0/reference#rave-parameters) to get the required field for each transaction

## Transaction
  This module retrieves all transactions and verifies transactions.

  *Usage*

  Import the transaction module
  
      from ravepaypysdk import Transaction
    

  - **Verify your transaction**

      *Usage*
      ```
      payload = {
        "flw_ref": "FLW-MOCK-6f52518a2ecca2b6b090f9593eb390ce", # unique reference for the transaction
        "tx_ref":"dummy", # merchants unique reference number
        "normalize": "1"
      }
      verify_transaction = Transaction.verify(payload, api=my_api)

      ```
  
  - **verify transaction with xquery**
      *Usage*
      ```
      payload = {
        "flwref": "FLW-MOCK-6f52518a2ecca2b6b090f9593eb390ce", # unique reference for the transaction
        "txref":"dummy", # merchants unique reference number
        "last_attempt":"1", # retrieves the last transaction
        "only_successful": "1" # retrieves only successful transaction
        }
      xquery_verify = Transaction.verify_query(payload, api=my_api)

      ```

  - **List all recurring transactions**

    *Usage*
    ```
    list_transactions  = Transaction.list_all_recurring(api=my_api)
    ```


  - **List single recurring transactions**
  
    *Usage*
    ```
    payload = {
        "txId":"dummy" #add the required value for txId
    }
    list_single_transaction = Transaction.list_single_recurring(payload, api=my_api)
    ```

## PreAuthorization
  This module performs preauthorization transactions on the RavePay platform

  *Usage*

  Import the PreAuthorization module
  ```
  from ravepaypysdk import PreAuthorization
  ```
  - **Preauthorization Capture**

    *Usage*
    ```
    payload = {
        "flwRef":"39448fhdhhfdhshshf" # add the required value
    }
    preauthorize_capture = PreAuthorization.capture(payload, api=my_api)
    ```

  
  - **Preauthorize Card transaction**

    *Usage*
    ```
    Payload is the same as direct charge card payment payload

    preauthorize_card = PreAuthorization.card(payload, api=my_api)

    ```


  - **Preauthorize void or refund transactions**

    *Usage*
    ```
    payload = {
        "flwRef":"dummy" # add the value from the capture response
        "action": "refund or void" # select what action i.e refund or void
    }
    preauth_void_refund = PreAuthorization.void_or_refund(payload, api=my_api)
    ```

    *Payload*

 ## Validate Ravepay charges
   This module validates RavePay payment transactions.

   *Usage*

   Import the ValidateCharge module

   ```
   from ravepaypysdk import ValidateCharge
   payload = {
        "transaction_reference": "222334304",
        "otp": "12345"
    }
   ```

  - **Validate card transactions**

    *Usage*
    ```

    validate_card_transac = ValidateCharge.card(payload, api=my_api)

    ```

  - **Validate bank account transaction**

    *Usage*
    ```
    validate_bank_account_transac = ValidateCharge.account(payload, api=my_api)
    ```

## Miscellanous 
  This module gets the bank list and current forex rates

  *Usage*

  Import the bank module

  ```
  from ravepaypysdk import Bank
  ```

  - **Get List of Banks**

    *Usage*
    ```
    get_banks = Bank.list_all(api=my_api)
    ```

  - **Get Forex Rates**

    *Usage*
    ```
    payload = {
     'origin_currency': 'USD',
     'destination_currency': 'NGN',
     'amount': '200'
     }
    get_forex = Bank.get_forex(payload, api=my_api)
    ```

## Documentation
API documentation for RavePay can be found [here](https://flutterwavedevelopers.readme.io/v1.0/reference#introduction)


## Contributing

Contributions are always welcomed to the project. Use Github Issue for requests.

- Fork the project to your repository then clone it to your local machine.
- Create a new branch and make the necessary enhancement to the features.
- If the you wish to update an existing enhancement submit a pull request.
- If you are unsure about certain areas in the project feel to ask for assistance.









    

