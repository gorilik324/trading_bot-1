import requests
import hmac
import hashlib
import time

class BitmediaAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://exchange.bitmedia.io'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, params):
        params['nonce'] = str(int(time.time() * 1000))
        message = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha512).hexdigest()
        headers = {'X-API-KEY': self.api_key, 'X-API-SIGNATURE': signature}
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
        endpoint = f"/api/v1/ticker?symbol={symbol}"
        return self._make_request('GET', endpoint)

    def get_order_book(self, symbol):
        endpoint = f"/api/v1/order_book?symbol={symbol}"
        return self._make_request('GET', endpoint)

    def get_balances(self):
        endpoint = '/api/v1/balance'
        return self._make_request('GET', endpoint)

    def place_order(self, symbol, side, type, quantity, price=None):
        endpoint = '/api/v1/order'
        params = {'symbol': symbol, 'quantity': quantity}
        if type == 'buy':
            params['
