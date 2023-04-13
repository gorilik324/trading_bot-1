import requests
import hmac
import hashlib
import time

class FTXAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://ftx.com/api'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, method, endpoint, params=None):
        if params is None:
            params = {}
        ts = int(time.time() * 1000)
        payload = f'{ts}{method}{endpoint}'
        if method == 'POST' and params:
            payload += json.dumps(params)
        signature = hmac.new(self.secret_key.encode(), payload.encode(), hashlib.sha256).hexdigest()
        headers = {
            'FTX-KEY': self.api_key,
            'FTX-SIGN': signature,
            'FTX-TS': str(ts)
        }
        return headers

    def _make_request(self, method, endpoint, params=None):
        url = self.base_url + endpoint
        headers = self._sign_request(method, endpoint, params)
        response = requests.request(method, url, headers=headers, json=params)
        response.raise_for_status()
        return response.json()

    def get_ticker(self, symbol):
        endpoint = f"/markets/{symbol}/"
        return self._make_request('GET', endpoint)

    def get_order_book(self, symbol, depth=20):
        endpoint = f"/markets/{symbol}/orderbook?depth={depth}"
        return self._make_request('GET', endpoint)

    def get_balances(self):
        endpoint = '/wallet/balances'
        return self._make_request('GET', endpoint)

    def place_order(self, symbol, side, type, quantity, price=None):
        endpoint = '/orders'
        params = {
            'market': symbol,
            'side': side,
            'type': type,
            'size': quantity,
            'price': price,
            'reduceOnly': False,
            'ioc': False,
            'postOnly': False,
        }
        return self._make_request('POST', endpoint, params=params)

    def cancel_order(self, order_id):
        endpoint = f'/orders/{order_id}'
        return self._make_request('DELETE', endpoint)
