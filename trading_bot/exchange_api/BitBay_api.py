import requests
import hmac
import hashlib
import time

class BitBayAPI:
def init(self, api_key, secret_key):
self.base_url = 'https://api.bitbay.net/rest'
self.api_key = api_key
self.secret_key = secret_key

python
Copy code
def _sign_request(self, params):
    params['time'] = str(int(time.time() * 1000))
    message = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
    signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha512).hexdigest()
    headers = {'API-Key': self.api_key, 'API-Hash': signature}
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
    endpoint = f"/trading/ticker/{symbol}"
    return self._make_request('GET', endpoint)

def get_order_book(self, symbol):
    endpoint = f"/trading/orderbook/{symbol}"
    return self._make_request('GET', endpoint)

def get_balances(self):
    endpoint = '/trading/accounts'
    params = {'currency': 'PLN,BTC'}
    return self._make_request('GET', endpoint, params=params)

def place_order(self, symbol, side, type, quantity, price=None):
    endpoint = '/trading/order'
    if type == 'buy':
        order_type = 'BID'
    else:
        order_type = 'ASK'
    params = {'market': symbol, 'type': order_type, 'amount': quantity, 'price': price}
    return self._make_request('POST', endpoint, params=params)

def cancel_order(self, order_id):
    endpoint = '/trading/cancel'
    params = {'id': order_id}
    return self._make_request('POST', endpoint, params=params)