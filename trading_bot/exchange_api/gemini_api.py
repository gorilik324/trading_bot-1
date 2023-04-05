import requests
import hmac
import hashlib
import time

class GeminiAPI:
def init(self, api_key, secret_key):
self.base_url = 'https://api.gemini.com'
self.api_key = api_key
self.secret_key = secret_key

python
Copy code
def _sign_request(self, payload):
    payload['nonce'] = str(int(time.time() * 1000))
    encoded_payload = str(payload).encode()
    b64 = base64.b64encode(encoded_payload).decode('utf-8')
    signature = hmac.new(self.secret_key.encode(), b64.encode(), hashlib.sha384).hexdigest()
    headers = {'Content-Type': 'text/plain',
               'Content-Length': '0',
               'X-GEMINI-APIKEY': self.api_key,
               'X-GEMINI-PAYLOAD': b64,
               'X-GEMINI-SIGNATURE': signature}
    return headers

def _make_request(self, method, endpoint, payload=None):
    url = self.base_url + endpoint
    headers = {}
    if payload:
        headers = self._sign_request(payload)
    response = requests.request(method, url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def get_ticker(self, symbol):
    endpoint = f"/v1/pubticker/{symbol}"
    return self._make_request('GET', endpoint)

def get_order_book(self, symbol):
    endpoint = f"/v1/book/{symbol}"
    return self._make_request('GET', endpoint)

def get_balances(self):
    endpoint = '/v1/balances'
    return self._make_request('POST', endpoint)

def place_order(self, symbol, side, type, quantity, price=None):
    endpoint = '/v1/order/new'
    payload = {'request': '/v1/order/new',
               'nonce': str(int(time.time() * 1000)),
               'symbol': symbol,
               'amount': str(quantity),
               'price': str(price),
               'side': side,
               'type': type}
    return self._make_request('POST', endpoint, payload)

def cancel_order(self, order_id):
    endpoint = '/v1/order/cancel'
    payload = {'request': '/v1/order/cancel',
               'nonce': str(int(time.time() * 1000)),
               'order_id': order_id}
    return self._make_request('POST', endpoint, payload)