import requests
import hmac
import hashlib
import time

class GateIOAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://api.gateio.ws/api/v4'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, params):
        query_string = '&'.join(f'{key}={value}' for key, value in params.items())
        signature = hmac.new(self.secret_key.encode(), query_string.encode(), hashlib.sha512).hexdigest()
        params['key'] = self.api_key
        params['sign'] = signature
        return params

    def _make_request(self, method, endpoint, params=None):
        url = self.base_url + endpoint
        headers = {'Content-Type': 'application/json'}
        if params:
            params = self._sign_request(params)
        response = requests.request(method, url, headers=headers, json=params)
        response.raise_for_status()
        return response.json()

    def get_account_info(self):
        endpoint = '/spot/accounts'
        return self._make_request('GET', endpoint)

    def get_trade_history(self, symbol, start_time=None, end_time=None):
        endpoint = f'/spot/trades?currency_pair={symbol}'
        if start_time:
            endpoint += f'&start_time={int(start_time * 1000)}'
        if end_time:
            endpoint += f'&end_time={int(end_time * 1000)}'
        return self._make_request('GET', endpoint)

    def place_order(self, symbol, side, type, amount, price=None):
        endpoint = '/spot/orders'
        params = {
            'currency_pair': symbol,
            'side': side,
            'type': type,
            'amount': str(amount),
            'time_in_force': 'gtc'
        }
        if price:
            params['price'] = str(price)
        return self._make_request('POST', endpoint, params=params)

    def cancel_order(self, order_id):
        endpoint = f'/spot/orders/{order_id}/cancel'
        return self._make_request('POST', endpoint)
