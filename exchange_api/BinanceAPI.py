import requests
import hmac
import hashlib
import time

class BinanceAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://api.binance.com/api/v3'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, params):
        query_string = '&'.join(f'{key}={value}' for key, value in params.items())
        signature = hmac.new(self.secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        params['signature'] = signature
        return params

    def _make_request(self, method, endpoint, params=None):
        url = self.base_url + endpoint
        headers = {'X-MBX-APIKEY': self.api_key}
        if params:
            params = self._sign_request(params)
        response = requests.request(method, url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_exchange_info(self):
        return self._make_request('GET', '/exchangeInfo')

    def get_klines(self, symbol, interval, limit=500):
        params = {'symbol': symbol, 'interval': interval, 'limit': limit}
        return self._make_request('GET', '/klines', params=params)

    def get_account_info(self):
        return self._make_request('GET', '/account')

    def place_order(self, symbol, side, type, quantity, price=None, time_in_force='GTC'):
        params = {'symbol': symbol, 'side': side, 'type': type, 'quantity': quantity, 'timeInForce': time_in_force}
        if price:
            params['price'] = price
        return self._make_request('POST', '/order', params=params)

    def cancel_order(self, symbol, order_id):
        params = {'symbol': symbol, 'orderId': order_id}
        return self._make_request('DELETE', '/order', params=params)
