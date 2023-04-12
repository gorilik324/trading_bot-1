import requests
import hmac
import hashlib
import time

class BTCCAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://api.btcc.com'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, params):
        query_string = '&'.join(f'{key}={value}' for key, value in params.items())
        signature = hmac.new(self.secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        params['sign'] = signature
        return params

    def _make_request(self, method, endpoint, params=None):
        url = self.base_url + endpoint
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'ACCESS_KEY': self.api_key,
                   'ACCESS_SIGN': '',
                   'ACCESS_NONCE': ''}
        if params:
            params = self._sign_request(params)
        nonce = str(int(time.time() * 1000))
        headers['ACCESS_NONCE'] = nonce
        message = nonce + method + endpoint
        if params:
            message += '&'.join([f"{key}={value}" for key, value in params.items()])
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
        headers['ACCESS_SIGN'] = signature
        response = requests.request(method, url, headers=headers, data=params)
        response.raise_for_status()
        return response.json()

    def get_exchange_info(self):
        return self._make_request('GET', '/data/v1/ticker')

    def get_klines(self, symbol, interval, limit=500):
        endpoint = f"/data/v1/klines?symbol={symbol}&interval={interval}&limit={limit}"
        return self._make_request('GET', endpoint)

    def get_account_info(self):
        endpoint = '/api/userinfo'
        return self._make_request('POST', endpoint)

    def place_order(self, symbol, side, type, quantity, price=None):
        endpoint = '/api/buy'
        if side == 'sell':
            endpoint = '/api/sell'
        params = {'coin': symbol, 'type': type, 'amount': quantity}
        if price:
            params['price'] = price
        return self._make_request('POST', endpoint, params=params)

    def cancel_order(self, symbol, order_id):
        endpoint = f'/api/cancel'
        params = {'id': order_id}
        return self._make_request('POST', endpoint, params=params)
