import requests
import hmac
import hashlib
import time

class HitBTCAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://api.hitbtc.com'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, params):
        params['nonce'] = str(int(time.time() * 1000))
        message = '/api' + params['url'] + '?' + '&'.join([f"{key}={params[key]}" for key in sorted(params)])
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha512).hexdigest()
        headers = {'Authorization': self.api_key, 'X-Signature': signature}
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
        endpoint = f"/api/3/public/ticker/{symbol}"
        return self._make_request('GET', endpoint)

    def get_order_book(self, symbol):
        endpoint = f"/api/3/public/orderbook/{symbol}"
        return self._make_request('GET', endpoint)

    def get_balances(self):
        endpoint = '/api/3/trading/balance'
        params = {}
        return self._make_request('GET', endpoint, params=params)

    def place_order(self, symbol, side, type, quantity, price=None):
        endpoint = '/api/3/order'
        params = {'symbol': symbol, 'side': side, 'type': type, 'quantity': quantity, 'timeInForce': 'FOK'}
        if price:
            params['price'] = price
        return self._make_request('POST', endpoint, params=params)

    def cancel_order(self, order_id):
        endpoint = f"/api/3/order/{order_id}"
        params = {}
        return self._make_request('DELETE', endpoint, params=params)
