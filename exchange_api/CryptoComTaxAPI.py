import requests
import hmac
import hashlib
import time

class CryptoComTaxAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://tax-api.crypto.com'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, params):
        params['nonce'] = str(int(time.time() * 1000))
        message = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
        headers = {'Content-Type': 'application/json', 'X-API-KEY': self.api_key, 'X-API-SIG': signature}
        return headers

    def _make_request(self, method, endpoint, params=None):
        url = self.base_url + endpoint
        headers = {}
        if params:
            headers = self._sign_request(params)
        response = requests.request(method, url, headers=headers, json=params)
        response.raise_for_status()
        return response.json()

    def get_trades(self, symbols, start_date, end_date):
        endpoint = '/v1/trades'
        params = {'symbols': symbols, 'startDate': start_date, 'endDate': end_date}
        return self._make_request('GET', endpoint, params=params)

    def get_fills(self, symbols, start_date, end_date):
        endpoint = '/v1/fills'
        params = {'symbols': symbols, 'startDate': start_date, 'endDate': end_date}
        return self._make_request('GET', endpoint, params=params)

    def get_balances(self):
        endpoint = '/v1/balances'
        return self._make_request('GET', endpoint)

    def place_order(self, symbol, side, type, quantity, price=None):
        endpoint = '/v1/orders'
        params = {'symbol': symbol, 'side': side, 'type': type, 'quantity': quantity}
        if price:
            params['price'] = price
        return self._make_request('POST', endpoint, params=params)

    def cancel_order(self, order_id):
        endpoint = f'/v1/orders/{order_id}/cancel'
        return self._make_request('POST', endpoint)

    def get_order_status(self, order_id):
        endpoint = f'/v1/orders/{order_id}/status'
        return self._make_request('GET', endpoint)
