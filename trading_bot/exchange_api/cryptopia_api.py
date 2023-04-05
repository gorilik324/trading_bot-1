import requests
import hmac
import hashlib
import time

class CryptopiaAPI:
def init(self, api_key, secret_key):
self.base_url = 'https://www.cryptopia.co.nz/api'
self.api_key = api_key
self.secret_key = secret_key

python
Copy code
def _sign_request(self, params):
    params['nonce'] = str(int(time.time()))
    message = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
    signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f"amx {self.api_key}:{signature}", 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Cryptopia Python API Client'}
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
    endpoint = f"/GetMarket/{symbol}/"
    return self._make_request('GET', endpoint)

def get_order_book(self, symbol):
    endpoint = f"/GetMarketOrders/{symbol}/"
    return self._make_request('GET', endpoint)

def get_balances(self):
    endpoint = '/GetBalance/'
    params = {}
    return self._make_request('POST', endpoint, params=params)

def place_order(self, symbol, side, type, quantity, price=None):
    endpoint = '/SubmitTrade/'
    params = {'Market': symbol, 'Type': type, 'Rate': price, 'Amount': quantity}
    if side == 'buy':
        params['Type'] = 'Buy'
    else:
        params['Type'] = 'Sell'
    return self._make_request('POST', endpoint, params=params)

def cancel_order(self, order_id):
    endpoint = '/CancelTrade/'
    params = {'Type': 'Trade', 'OrderId': order_id}
    return self._make_request('POST', endpoint, params=params)