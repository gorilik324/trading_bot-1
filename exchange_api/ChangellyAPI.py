import requests
import hmac
import hashlib
import time
import json

class ChangellyAPI:
def init(self, api_key, secret_key):
self.base_url = 'https://api.changelly.com/v1'
self.api_key = api_key
self.secret_key = secret_key

python
Copy code
def _sign_request(self, params):
    message = json.dumps(params)
    signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha512).hexdigest()
    headers = {'api-key': self.api_key, 'sign': signature, 'Content-Type': 'application/json'}
    return headers

def _make_request(self, method, endpoint, params=None):
    url = self.base_url + endpoint
    headers = {}
    if params:
        headers = self._sign_request(params)
    response = requests.request(method, url, headers=headers, json=params)
    response.raise_for_status()
    return response.json()

def get_pairs(self):
    endpoint = '/public/getPairs'
    return self._make_request('POST', endpoint)

def get_min_amount(self, from_currency, to_currency):
    endpoint = '/public/minAmount'
    params = {'from': from_currency, 'to': to_currency}
    return self._make_request('POST', endpoint, params=params)

def get_exchange_amount(self, from_currency, to_currency, amount):
    endpoint = '/public/estimate'
    params = {'from': from_currency, 'to': to_currency, 'amount': amount}
    return self._make_request('POST', endpoint, params=params)

def create_transaction(self, from_currency, to_currency, from_address, to_address, amount):
    endpoint = '/exchange/createTransaction'
    params = {'from': from_currency, 'to': to_currency, 'fromAddress': from_address, 'toAddress': to_address, 'amount': amount}
    return self._make_request('POST', endpoint, params=params)

def get_status(self, transaction_id):
    endpoint = '/exchange/status'
    params = {'id': transaction_id}
    return self._make_request('POST', endpoint, params=params)