import requests
import hmac
import hashlib
import time

class CCEXAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://c-cex.com/t'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, params):
        params['apikey'] = self.api_key
        params['nonce'] = str(int(time.time()))
        message = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha512).hexdigest()
        headers = {'apisign': signature}
        return headers

    def _make_request(self, method, endpoint, params=None):
        url = self.base_url + endpoint
        headers = {}
        if params:
            headers = self._sign_request(params)
        response = requests.request(method, url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_ticker(self, symbol):
        endpoint = f"/api_pub.html?a=getticker&market={symbol}"
        return self._make_request('GET', endpoint)

    def get_order_book(self, symbol):
        endpoint = f"/api_pub.html?a=getorderbook&market={symbol}&type=both"
        return self._make_request('GET', endpoint)

    def get_balances(self):
        endpoint = '/api.html'
        params = {'a': 'getbalances'}
        return self._make_request('POST', endpoint, params=params)

    def place_order(self, symbol, side, type, quantity, price=None):
        endpoint = '/api.html'
        params = {'a': 'submitorder', 'market': symbol, 'quantity': quantity}
        if type == 'buy':
            params['type'] = 'buy'
        else:
            params['type'] = 'sell'
        if price:
            params['rate'] = price
        return self._make_request('POST', endpoint, params=params)

    def cancel_order(self, order_id):
        endpoint = '/api.html'
        params = {'a': 'cancelorder', 'orderid': order_id}
        return self._make_request('POST', endpoint, params=params)
