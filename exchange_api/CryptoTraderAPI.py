import requests
import hmac
import hashlib
import time

class CryptoTraderAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://api.crypto.com/v2'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, params):
        params['nonce'] = str(int(time.time() * 1000))
        message = ''.join([f"{key}{params[key]}" for key in sorted(params)])
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
        headers = {'Content-Type': 'application/json', 'X-MKT-APIKEY': self.api_key, 'X-MKT-SIGNATURE': signature}
        return headers

    def _make_request(self, method, endpoint, params=None):
        url = self.base_url + endpoint
        headers = {}
        if params:
            headers = self._sign_request(params)
        response = requests.request(method, url, headers=headers, json=params)
        response.raise_for_status()
        return response.json()

    def get_ticker(self, symbol):
        endpoint = f"/public/get-ticker?instrument_name={symbol}"
        return self._make_request('GET', endpoint)

    def get_order_book(self, symbol):
        endpoint = f"/public/get-order-book?instrument_name={symbol}"
        return self._make_request('GET', endpoint)

    def get_balances(self):
        endpoint = '/private/get-account-summary'
        params = {'currency': 'ALL'}
        return self._make_request('POST', endpoint, params=params)

    def place_order(self, symbol, side, type, quantity, price=None):
        endpoint = '/private/create-order'
        params = {'instrument_name': symbol, 'side': side, 'type': type, 'quantity': quantity}
        if price:
            params['price'] = price
        return self._make_request('POST', endpoint, params=params)

    def cancel_order(self, order_id):
        endpoint = '/private/cancel-order'
        params = {'order_id': order_id}
        return self._make_request('POST', endpoint, params=params)
