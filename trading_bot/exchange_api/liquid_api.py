import requests
import hmac
import hashlib
import time

class LiquidAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://api.liquid.com'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, method, endpoint, params=None):
        nonce = str(int(time.time() * 1000))
        if params is None:
            params = {}
        path = f"/api{endpoint}"
        body = '' if method == 'GET' else str(params)
        message = nonce + method + path + body
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
        headers = {
            'X-Quoine-API-Version': '2',
            'X-Quoine-Auth': f"{self.api_key}:{signature}:{nonce}",
            'Content-Type': 'application/json'
        }
        return headers

    def _make_request(self, method, endpoint, params=None):
        url = self.base_url + endpoint
        headers = self._sign_request(method, endpoint, params)
        response = requests.request(method, url, headers=headers, json=params)
        response.raise_for_status()
        return response.json()

    def get_ticker(self, symbol):
        endpoint = f"/products/{symbol}/price_levels"
        return self._make_request('GET', endpoint)

    def get_order_book(self, symbol):
        endpoint = f"/products/{symbol}/price_levels"
        return self._make_request('GET', endpoint)

    def get_balances(self):
        endpoint = '/accounts/balance'
        return self._make_request('GET', endpoint)

    def place_order(self, symbol, side, type, quantity, price=None):
        endpoint = '/orders'
        params = {
            'currency_pair_code': symbol,
            'side': side,
            'quantity': str(quantity),
            'order_type': type,
            'product_id': '1'  # Default value for spot trading
        }
        if price is not None:
            params['price'] = str(price)
        return self._make_request('POST', endpoint, params)

    def cancel_order(self, order_id):
        endpoint = f"/orders/{order_id}/cancel"
        return self._make_request('PUT', endpoint)
