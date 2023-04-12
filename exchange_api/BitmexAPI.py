import requests
import hmac
import hashlib
import time

class BitmexAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://www.bitmex.com/api/v1'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, verb, path, expires, data):
        message = verb + path + str(expires) + data
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
        return {
            'api-expires': str(expires),
            'api-key': self.api_key,
            'api-signature': signature
        }

    def _make_request(self, verb, path, data=None):
        expires = int(time.time()) + 60
        url = self.base_url + path
        headers = self._sign_request(verb, path, expires, data) if data else {}
        headers['content-type'] = 'application/json'
        headers['accept'] = 'application/json'
        headers['api-expires'] = str(expires)
        headers['api-key'] = self.api_key
        headers['api-signature'] = hmac.new(self.secret_key.encode(), (verb + path + str(expires)).encode(), hashlib.sha256).hexdigest()
        response = requests.request(verb, url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()

    def get_ticker(self, symbol):
        endpoint = f"/instrument?symbol={symbol}&columns=lastPrice"
        return self._make_request('GET', endpoint)

    def get_order_book(self, symbol, depth=25):
        endpoint = f"/orderBook/L2?symbol={symbol}&depth={depth}"
        return self._make_request('GET', endpoint)

    def get_balances(self):
        endpoint = '/user/wallet'
        return self._make_request('GET', endpoint)

    def place_order(self, symbol, side, type, quantity, price=None):
        endpoint = '/order'
        data = {
            'symbol': symbol,
            'side': side,
            'orderQty': quantity,
            'ordType': type
        }
        if price:
            data['price'] = price
        return self._make_request('POST', endpoint, data=data)

    def cancel_order(self, order_id):
        endpoint = f"/order/{order_id}"
        return self._make_request('DELETE', endpoint)
