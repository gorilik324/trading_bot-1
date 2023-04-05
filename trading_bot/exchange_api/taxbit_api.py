import requests
import hmac
import hashlib
import time

class TaxBitAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://api.taxbit.com'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, params):
        params['nonce'] = str(int(time.time() * 1000))
        message = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha512).hexdigest()
        headers = {'X-Taxbit-Api-Key': self.api_key, 'X-Taxbit-Signature': signature, 'X-Taxbit-Nonce': params['nonce']}
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
        endpoint = f"/v1/market-data/ticker?symbol={symbol}"
        return self._make_request('GET', endpoint)

    def get_order_book(self, symbol):
        endpoint = f"/v1/market-data/order-book?symbol={symbol}"
        return self._make_request('GET', endpoint)

    def get_balances(self):
        endpoint = '/v1/accounts/balances'
        return self._make_request('GET', endpoint)

    def place_order(self, symbol, side, type, quantity, price=None):
        endpoint = '/v1/orders'
        params = {'symbol': symbol, 'side': side, 'type': type, 'quantity': quantity, 'timeInForce': 'GTC'}
        if price:
            params['price'] = price
        return self._make_request('POST', endpoint, params=params)

    def cancel_order(self, order_id):
        endpoint = f'/v1/orders/{order_id}'
        return self._make_request('DELETE', endpoint)
