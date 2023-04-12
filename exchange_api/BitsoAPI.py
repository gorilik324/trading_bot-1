import requests
import hmac
import hashlib
import base64
import time

class BitsoAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://api.bitso.com/v3'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, method, path, body=''):
        nonce = str(int(time.time() * 1000))
        message = f"{nonce}{method.upper()}{path}{body}\n"
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).digest()
        encoded_signature = base64.b64encode(signature).decode()
        headers = {'Authorization': f'Bitso {self.api_key}:{encoded_signature}', 'Content-Type': 'application/json'}
        return headers

    def _make_request(self, method, endpoint, params=None, body=None):
        url = self.base_url + endpoint
        headers = {}
        if params:
            query_string = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
            url = f"{url}?{query_string}"
        if body:
            headers['Content-Type'] = 'application/json'
        headers.update(self._sign_request(method, endpoint, body))
        response = requests.request(method, url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()

    def get_ticker(self, symbol):
        endpoint = f"/ticker/?book={symbol}"
        return self._make_request('GET', endpoint)

    def get_order_book(self, symbol):
        endpoint = f"/order_book/?book={symbol}"
        return self._make_request('GET', endpoint)

    def get_balances(self):
        endpoint = '/balance/'
        return self._make_request('GET', endpoint)

    def place_order(self, symbol, side, quantity, price=None):
        if price:
            endpoint = '/orders/'
            params = {'book': symbol, 'side': side, 'type': 'limit', 'major': quantity, 'price': price}
        else:
            endpoint = '/orders/market/'
            params = {'book': symbol, 'side':
