import requests
import hashlib
import hmac
import time

class NiceHashAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = 'https://api2.nicehash.com'

    def _sign_request(self, endpoint, data):
        message = endpoint + chr(0).encode() + data.encode() + chr(0).encode() + str(time.time()).split('.')[0].encode()
        signature = hmac.new(self.api_secret.encode(), message, hashlib.sha256).hexdigest()
        return {'X-Time': str(time.time()).split('.')[0], 'X-Organization-Access-Key': self.api_key, 'X-Nonce': str(int(time.time())), 'X-Signature': signature}

    def _make_request(self, method, endpoint, data=None):
        url = self.base_url + endpoint
        headers = {'Content-Type': 'application/json', 'X-Time': '', 'X-Organization-Access-Key': '', 'X-Nonce': '', 'X-Signature': ''}
        if data:
            headers.update(self._sign_request(endpoint, data))
        response = requests.request(method, url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()

    def get_exchange_info(self):
        return self._make_request('GET', '/main/api/v2/public/exchange/coin/info')

    def get_market_depth(self, market, limit=50):
        return self._make_request('GET', f'/exchange/api/v2/info/orderbook?market={market}&limit={limit}')

    def get_account_info(self):
        return self._make_request('GET', '/main/api/v2/accounting/accounts2')

    def place_order(self, market, side, order_type, quantity, price=None, time_in_force='GTC'):
        data = {'market': market, 'side': side, 'type': order_type, 'quantity': str(quantity), 'time_in_force': time_in_force}
        if price:
            data['price'] = str(price)
        return self._make_request('POST', '/exchange/api/v2/order', data=data)

    def cancel_order(self, order_id):
        return self._make_request('DELETE', f'/exchange/api/v2/order/{order_id}')
