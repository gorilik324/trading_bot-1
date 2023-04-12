import requests
import hmac
import hashlib
import base64
import time

class FBSAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://api.fbs.eu'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, params):
        params['timestamp'] = str(int(time.time() * 1000))
        message = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).digest()
        signature = base64.b64encode(signature).decode()
        headers = {'Authorization': f"Bearer {self.api_key}", 'Signature': signature}
        return headers

    def _make_request(self, method, endpoint, params=None):
        url = self.base_url + endpoint
        headers = {}
        if params:
            headers = self._sign_request(params)
        response = requests.request(method, url, headers=headers, json=params)
        response.raise_for_status()
        return response.json()

    def get_ticker(self, symbol):
        endpoint = f"/api/v2/quote/{symbol}"
        return self._make_request('GET', endpoint)

    def get_order_book(self, symbol):
        endpoint = f"/api/v2/depth/{symbol}"
        return self._make_request('GET', endpoint)

    def get_balances(self):
        endpoint = '/api/v2/me/accounts'
        return self._make_request('GET', endpoint)

    def place_order(self, symbol, side, type, quantity, price=None):
        endpoint = '/api/v2/trading/orders'
        params = {'symbol': symbol, 'side': side, 'type': type, 'volume': quantity}
        if price is not None:
            params['price'] = price
        return self._make_request('POST', endpoint, params=params)

    def cancel_order(self, order_id):
        endpoint = f"/api/v2/trading/orders/{order_id}"
        return self._make_request('DELETE', endpoint)
