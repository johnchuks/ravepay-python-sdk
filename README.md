# RavePay-SDK-Python
[![Build Status](https://travis-ci.org/johnchuks/RavePay-SDK-Python.svg?branch=master)](https://travis-ci.org/johnchuks/RavePay-SDK-Python)

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/johnchuks/RavePay-SDK-Python/badges/quality-score.png?b=sdk-docs)](https://scrutinizer-ci.com/g/johnchuks/RavePay-SDK-Python/?branch=sdk-docs)

[![Coverage Status](https://coveralls.io/repos/github/johnchuks/RavePay-SDK-Python/badge.svg?branch=master)](https://coveralls.io/github/johnchuks/RavePay-SDK-Python?branch=master)

[![Code Intelligence Status](https://scrutinizer-ci.com/g/johnchuks/RavePay-SDK-Python/badges/code-intelligence.svg?b=sdk-docs)](https://scrutinizer-ci.com/code-intelligence)

The RavePay Python SDK provides APIs to create, process and manage payments on the RavePay platform. The SDK fully supports the API

## Installation
`pip install ravepaypysdk`

## Configuring RavePay SDK
```
import ravepaypysdk

my_api = ravepaypysdk.Api(
          SECRET_KEY='ravepay_secret_key'
          PUBLIC_KEY='ravepay_public_key'
          Production=False # sandbox # or True # Live
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
  - The same format goes for the **USSD**, **MPESA** and **Ghana Mobile Money**. Kindly review the API documentation to get the required field for each transaction

## Transaction
    Import the transaction module
    ```
    from ravepaypysdk import Transaction
    ```

  - **Verify transaction**

      *Usage*
      ```
      verify_transaction = Transaction.verify(payload, api=my_api)

      ```
      *Arguments*

        - Payload 
  
  - **verify transaction with xquery**
      *Usage*
      ```
      xquery_verify = Transaction.verify_query(payload, api=my_api)

      ```
      *Arguments*

  - **List all recurring transactions**
    *Usage*
    ```
    from ravepaypysdk import Transaction

    list_transactions  = Transaction.list_all_recurring(payload, api=my_api)
    ```
    *Arguments*

  - **List single recurring transactions**
    *Usage*
    ```
    list_single_transaction = Transaction.list_single_recurring(payload, api=my_api)
    ```
     *Payload*

## Preauthorization 
  Import the Preauthorization module
  ```
  from ravepaypysdk import Preauthorization
  ```
  - **Preauthorization Capture**

    *Usage*
    ```
    preauthorize_capture = Preauthorization.capture(payload, api=my_api)
    ```
    *Payload*
  
  - **Preauthorize Card transaction**

    *Usage*
    ```
    preauthorize_card = Preauthorization.card(payload, api=my_api)

    ```
    *Payload*

  - **Preauthorize void or refund transactions**

    *Usage*
    ```
    preauth_void_refund = Preauthorization.void_or_refund(payload, api=my_api)
    ```

    *Payload*

 ## Validate Ravepay charges
    Import the validation module

    ```
    from ravepaypysdk import ValidateCharge

    ```

    This interface helps in validating transaction made through the RavePay platform

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
  Miscellanous includes getting the current forex rate and lists of banks supported by the RavePay Platform

  Import the bank module to get list of banks and current forex rates

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
    get_forex = Bank.get_forex(api=my_api)
    ```









    

