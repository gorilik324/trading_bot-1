import requests
import hmac
import hashlib
import time

class OKXAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://www.okex.com/api'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, params):
        params['api_key'] = self.api_key
        query_string = '&'.join(f'{key}={value}' for key, value in params.items())
        signature = hmac.new(self.secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        params['sign'] = signature
        return params

    def _make_request(self, method, endpoint, params=None):
        url = self.base_url + endpoint
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        if params:
            params = self._sign_request(params)
        response = requests.request(method, url, headers=headers, data=params)
        response.raise_for_status()
        return response.json()

    def get_exchange_info(self):
        return self._make_request('GET', '/v1/exchange_info.do')

    def get_klines(self, symbol, interval, limit=500):
        params = {'symbol': symbol, 'type': interval, 'size': limit}
        return self._make_request('GET', '/v1/kline.do', params=params)

    def get_account_info(self):
        params = {'api_key': self.api_key}
        return self._make_request('POST', '/v1/userinfo.do', params=params)

    def place_order(self, symbol, side, type, quantity, price=None):
        params = {'symbol': symbol, 'type': type, 'side': side, 'amount': quantity}
        if price:
            params['price'] = price
        return self._make_request('POST', '/v1/trade.do', params=params)

    def cancel_order(self, symbol, order_id):
        params = {'symbol': symbol, 'order_id': order_id}
        return self._make_request('POST', '/v1/cancel_order.do', params=params)
