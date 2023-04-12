import requests
import hmac
import hashlib
import time

class Bit2cAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://bit2c.co.il/Exchanges/'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, params):
        params['nonce'] = str(int(time.time() * 1000))
        message = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha512).hexdigest()
        headers = {'ACCESS_KEY': self.api_key, 'ACCESS_SIGNATURE': signature}
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
        endpoint = f"{symbol}/Ticker.json"
        return self._make_request('GET', endpoint)

    def get_order_book(self, symbol):
        endpoint = f"{symbol}/Orderbook.json"
        return self._make_request('GET', endpoint)

    def get_balances(self):
        endpoint = '/Account/Balance.json'
        params = {'nonce': int(time.time() * 1000)}
        return self._make_request('POST', endpoint, params=params)

    def place_order(self, symbol, side, type, quantity, price=None):
        endpoint = '/Order/AddOrder.json'
        params = {'Amount': quantity, 'Price': price, 'IsBid': 1 if type == 'buy' else 0, 'Currency': symbol}
        headers = self._sign_request(params)
        return self._make_request('POST', endpoint, params=params)

    def cancel_order(self, order_id):
        endpoint = '/Order/CancelOrder.json'
        params = {'oid': order_id}
        return self._make_request('POST', endpoint, params=params)
