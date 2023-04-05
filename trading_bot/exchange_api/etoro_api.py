import requests
import time
import json

class EToroAPI:
def init(self, client_id, secret_key):
self.base_url = 'https://api.etoro.com'
self.client_id = client_id
self.secret_key = secret_key

python
Copy code
def _make_request(self, method, endpoint, params=None):
    url = self.base_url + endpoint
    headers = {'Content-Type': 'application/json',
               'X-User-Type': 'Client',
               'X-Partner-ID': self.client_id,
               'X-Partner-Token': '',
               'X-Date': ''}
    if params:
        params = json.dumps(params)
    timestamp = str(int(time.time()))
    headers['X-Date'] = timestamp
    message = method + '\n' + timestamp + '\n' + endpoint
    if params:
        message += '\n' + params
    signature = self._sign_request(message)
    headers['X-Partner-Token'] = signature
    response = requests.request(method, url, headers=headers, data=params)
    response.raise_for_status()
    return response.json()

def _sign_request(self, message):
    signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha1).digest()
    return signature.hex()

def get_market_data(self, instrument_id):
    endpoint = f'/api/v1/instruments/{instrument_id}/candles/daily'
    params = {'client_request_id': str(int(time.time()))}
    return self._make_request('GET', endpoint, params=params)

def get_account_summary(self):
    endpoint = '/api/v1/users/portfolio'
    return self._make_request('GET', endpoint)

def place_order(self, instrument_id, direction, amount, leverage):
    endpoint = '/api/v1/trade-orders'
    params = {'instrument_id': instrument_id, 'direction': direction, 'leverage': leverage, 'amount': amount}
    return self._make_request('POST', endpoint, params=params)

def close_position(self, position_id):
    endpoint = f'/api/v1/trade-orders/{position_id}'
    return self._make_request('DELETE', endpoint) 