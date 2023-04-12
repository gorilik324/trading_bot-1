import requests
import hmac
import hashlib
import time

class ChangeNowAPI:
def init(self, api_key, secret_key):
self.base_url = 'https://changenow.io/api/v1'
self.api_key = api_key
self.secret_key = secret_key

python
Copy code
def _sign_request(self, params):
    params['nonce'] = str(int(time.time() * 1000))
    message = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
    signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha512).hexdigest()
    headers = {'api-key': self.api_key, 'sign': signature}
    return headers

def _make_request(self, method, endpoint, params=None):
    url = self.base_url + endpoint
    headers = {}
    if params:
        headers = self._sign_request(params)
    response = requests.request(method, url, headers=headers, json=params)
    response.raise_for_status()
    return response.json()

def get_ticker(self, input_currency, output_currency):
    endpoint = f"/{input_currency}_{output_currency}/rate"
    return self._make_request('GET', endpoint)

def get_order_limits(self, input_currency, output_currency):
    endpoint = f"/{input_currency}_{output_currency}/limits"
    return self._make_request('GET', endpoint)

def create_transaction(self, input_currency, output_currency, input_amount, output_amount, destination_address, refund_address=None):
    endpoint = "/transactions"
    params = {'from': input_currency, 'to': output_currency, 'amount': input_amount, 'address': destination_address}
    if refund_address:
        params['refundAddress'] = refund_address
    return self._make_request('POST', endpoint, params=params)

def get_transaction_status(self, transaction_id):
    endpoint = f"/transactions/{transaction_id}/status"
    return self._make_request('GET', endpoint)

def get_transaction_info(self, transaction_id):
    endpoint = f"/transactions/{transaction_id}"
    return self._make_request('GET', endpoint)

def get_currencies(self):
    endpoint = "/currencies"
    return self._make_request('GET', endpoint)