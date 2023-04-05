import requests
import hmac
import hashlib
import time

class CryptoViewAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://cryptoview.com/api/v1'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, params):
        params['nonce'] = str(int(time.time() * 1000))
        message = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha512).hexdigest()
        headers = {'X-API-KEY': self.api_key, 'X-API-SIGNATURE': signature}
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
        endpoint = f"/public/markets/ticker/{symbol}"
        return self._make_request('GET', endpoint)

    def get_order_book(self, symbol):
        endpoint = f"/public/markets/order-book/{symbol}"
        return self._make_request('GET', endpoint)

    def get_balances(self):
        endpoint = '/account/balance'
        return self._make_request('GET', endpoint)

    def place_order(self, symbol, side, type, quantity, price=None):
        endpoint = '/account/order'
        params = {'market_symbol': symbol, 'side': side, 'type': type, 'quantity': quantity, 'clientOrderId': int(time.time() * 1000)}
        if price:
            params['price'] = price
        return self._make_request('POST', endpoint, params=params)

    def cancel_order(self, order_id):
        endpoint = f'/account/order/{order_id}'
        return self._make_request('DELETE', endpoint)
