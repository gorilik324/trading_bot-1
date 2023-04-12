import requests
import hmac
import hashlib
import time

class TheRockTradingAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://api.therocktrading.com/v1'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, verb, path, body):
        nonce = str(int(time.time() * 1000))
        message = nonce + verb + path + (body or '')
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha384).hexdigest()
        headers = {
            'Content-Type': 'application/json',
            'X-TRT-KEY': self.api_key,
            'X-TRT-NONCE': nonce,
            'X-TRT-SIGN': signature
        }
        return headers

    def _make_request(self, verb, endpoint, params=None):
        url = self.base_url + endpoint
        body = ''
        if params:
            body = str(params)
        headers = self._sign_request(verb, endpoint, body)
        response = requests.request(verb, url, headers=headers, data=body)
        response.raise_for_status()
        return response.json()

    def get_ticker(self, symbol):
        endpoint = f"/funds/{symbol}/ticker"
        return self._make_request('GET', endpoint)

    def get_order_book(self, symbol):
        endpoint = f"/funds/{symbol}/orderbook"
        return self._make_request('GET', endpoint)

    def get_balances(self):
        endpoint = '/balances'
        return self._make_request('GET', endpoint)

    def place_order(self, symbol, side, type, quantity, price=None):
        endpoint = '/orders'
        params = {
            'fund_id': symbol,
            'side': side,
            'type': type,
            'amount': quantity,
            'price': price,
            'time_in_force': 'GTC'
        }
        return self._make_request('POST', endpoint, params=params)

    def cancel_order(self, order_id):
        endpoint = f'/orders/{order_id}/cancel'
        return self._make_request('POST', endpoint)
