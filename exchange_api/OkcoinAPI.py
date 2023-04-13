import requests
import hmac
import hashlib
import time

class OkcoinAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://www.okcoin.com'
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
                   'OK-ACCESS-KEY': self.api_key,
                   'OK-ACCESS-SIGN': '',
                   'OK-ACCESS-TIMESTAMP': ''}
        if params:
            params = self._sign_request(params)
        timestamp = str(int(time.time() * 1000))
        headers['OK-ACCESS-TIMESTAMP'] = timestamp
        message = timestamp + method + endpoint
        if params:
            message += '&'.join([f"{key}={value}" for key, value in params.items()])
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
        headers['OK-ACCESS-SIGN'] = signature
        response = requests.request(method, url, headers=headers, data=params)
        response.raise_for_status()
        return response.json()

    def get_exchange_info(self):
        return self._make_request('GET', '/api/v5/public/instruments')

    def get_klines(self, symbol, interval, limit=500):
        endpoint = f"/api/v5/market/candles?instId={symbol}&bar={interval}&limit={limit}"
        return self._make_request('GET', endpoint)

    def get_account_info(self):
        endpoint = '/api/v5/account/balance'
        return self._make_request('GET', endpoint)

    def place_order(self, symbol, side, type, quantity, price=None, time_in_force='GTC'):
        endpoint = '/api/v5/trade/order'
        params = {'instId': symbol, 'side': side, 'ordType': type, 'sz': quantity, 'tgtCcy': 'USDT'}
        if price:
            params['px'] = price
        return self._make_request('POST', endpoint, params=params)

    def cancel_order(self, symbol, order_id):
        endpoint = f'/api/v5/trade/cancel-order/{symbol}/{order_id}'
        return self._make_request('POST', endpoint)
