import requests
import hmac
import hashlib
import time

class WEXAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://wex.nz'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, params):
        params['nonce'] = str(int(time.time()))
        message = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha512).hexdigest()
        headers = {'Key': self.api_key, 'Sign': signature}
        return headers

    def _make_request(self, method, endpoint, params=None):
        url = self.base_url + endpoint
        headers = {}
        if params:
            headers = self._sign_request(params)
        response = requests.request(method, url, headers=headers, data=params)
        response.raise_for_status()
        return response.json()

    def get_ticker(self, symbol):
        endpoint = f"/api/3/ticker/{symbol}"
        return self._make_request('GET', endpoint)

    def get_order_book(self, symbol):
        endpoint = f"/api/3/depth/{symbol}"
        return self._make_request('GET', endpoint)

    def get_balances(self):
        endpoint = '/tapi'
        params = {'method': 'getInfo'}
        return self._make_request('POST', endpoint, params=params)

    def place_order(self, symbol, side, type, quantity, price=None):
        endpoint = '/tapi'
        params = {'method': 'Trade', 'pair': symbol, 'rate': price, 'amount': quantity}
        if type == 'buy':
            params['type'] = 'buy'
        else:
            params['type'] = 'sell'
        return self._make_request('POST', endpoint, params=params)

    def cancel_order(self, order_id):
        endpoint = '/tapi'
        params = {'method': 'CancelOrder', 'order_id': order_id}
        return self._make_request('POST', endpoint, params=params)
