import requests
import hmac
import hashlib
import time

class CexioAPI:
def init(self, api_key, secret_key):
self.base_url = 'https://cex.io'
self.api_key = api_key
self.secret_key = secret_key.encode()

python
Copy code
def _sign_request(self, params):
    nonce = str(int(time.time() * 1000))
    message = nonce + self.api_key + self.secret_key
    signature = hmac.new(self.secret_key, message.encode(), hashlib.sha256).hexdigest().upper()
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'application/json',
               'CEX-KEY': self.api_key,
               'CEX-SIGNATURE': signature,
               'CEX-NONCE': nonce}
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
    endpoint = f"/api/ticker/{symbol}/"
    return self._make_request('GET', endpoint)

def get_order_book(self, symbol):
    endpoint = f"/api/order_book/{symbol}/"
    return self._make_request('GET', endpoint)

def get_balances(self):
    endpoint = '/api/balance/'
    return self._make_request('POST', endpoint)

def place_order(self, symbol, side, type, quantity, price=None):
    endpoint = '/api/place_order/{symbol}/'
    params = {'type': type, 'amount': quantity}
    if price:
        params['price'] = price
    if side == 'buy':
        params['type'] = 'buy'
    else:
        params['type'] = 'sell'
    return self._make_request('POST', endpoint, params=params)

def cancel_order(self, order_id):
    endpoint = f"/api/cancel_order/{order_id}/"
    return self._make_request('POST', endpoint)