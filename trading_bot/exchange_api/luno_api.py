import requests
import hmac
import hashlib
import time

class LunoAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://api.luno.com/api/1'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, data):
        nonce = str(int(time.time() * 1e6))
        payload = nonce + self.base_url + data
        signature = hmac.new(self.secret_key.encode(), payload.encode(), hashlib.sha256).hexdigest()
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f"{self.api_key}:{signature}"}
        return headers

    def _make_request(self, method, endpoint, data=None):
        url = self.base_url + endpoint
        headers = self._sign_request(data or '')
        response = requests.request(method, url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()

    def get_ticker(self, pair):
        return self._make_request('GET', f'/ticker?pair={pair}')

    def get_order_book(self, pair):
        return self._make_request('GET', f'/orderbook?pair={pair}')

    def place_order(self, pair, type, volume, price=None):
        if price:
            data = f"pair={pair}&type={type}&volume={volume}&price={price}"
        else:
            data = f"pair={pair}&type={type}&volume={volume}"
        return self._make_request('POST', '/postorder', data=data)

    def cancel_order(self, order_id):
        data = f"order_id={order_id}"
        return self._make_request('POST', '/stoporder', data=data)
