import requests
import hmac
import hashlib
import time

class BybitAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://api.bybit.com/v2'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, params):
        query_string = '&'.join(f'{key}={value}' for key, value in params.items())
        signature = hmac.new(self.secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        params['sign'] = signature
        return params

    def _make_request(self, method, endpoint, params=None):
        url = self.base_url + endpoint
        headers = {'api-key': self.api_key}
        if params:
            params = self._sign_request(params)
        response = requests.request(method, url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_exchange_info(self):
        return self._make_request('GET', '/public/tickers')

    def get_klines(self, symbol, interval, limit=500):
        params = {'symbol': symbol, 'interval': interval, 'limit': limit}
        return self._make_request('GET', '/public/kline/list', params=params)
        
    def get_historical_klines(self, symbol, interval, start_time, end_time, limit=500):
        params = {'symbol': symbol, 'interval': interval, 'from': start_time, 'to': end_time, 'limit': limit}
        return self._make_request('GET', '/public/kline/list', params=params)
        
    def get_account_info(self):
        return self._make_request('GET', '/private/account')

    def place_order(self, symbol, side, type, quantity, price=None, time_in_force='GTC'):
        params = {'symbol': symbol, 'side': side, 'order_type': type, 'qty': quantity, 'time_in_force': time_in_force}
        if price:
            params['price'] = price
        return self._make_request('POST', '/private/order/create', params=params)

    def cancel_order(self, symbol, order_id):
        params = {'symbol': symbol, 'order_id': order_id}
        return self._make_request('POST', '/private/order/cancel', params=params)
