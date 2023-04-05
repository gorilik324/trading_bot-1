import requests
import hashlib
import hmac
import time

class KuCoinAPI:
    def __init__(self, api_key, secret_key, passphrase):
        self.base_url = 'https://api.kucoin.com'
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def _sign_request(self, method, endpoint, data=None):
        timestamp = str(int(time.time() * 1000))
        if data is None:
            data = ''
        if isinstance(data, (dict, list)):
            data = json.dumps(data)
        signature = '{}{}{}{}'.format(timestamp, method.upper(), endpoint, data)
        signature = signature.encode('utf-8')
        secret_key = self.secret_key.encode('utf-8')
        signature = hmac.new(secret_key, signature, hashlib.sha256).hexdigest()
        return {
            'KC-API-KEY': self.api_key,
            'KC-API-SIGN': signature,
            'KC-API-TIMESTAMP': timestamp,
            'KC-API-PASSPHRASE': self.passphrase
        }

    def _make_request(self, method, endpoint, data=None):
        url = self.base_url + endpoint
        headers = self._sign_request(method, endpoint, data)
        if data is not None:
            headers['Content-Type'] = 'application/json'
        response = requests.request(method, url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()

    def get_exchange_info(self):
        return self._make_request('GET', '/api/v1/symbols')

    def get_klines(self, symbol, interval, start_time=None, end_time=None, limit=None):
        params = {'symbol': symbol, 'type': interval}
        if start_time:
            params['startAt'] = start_time
        if end_time:
            params['endAt'] = end_time
        if limit:
            params['pageSize'] = limit
        return self._make_request('GET', '/api/v1/klines', data=params)

    def get_account_info(self):
        return self._make_request('GET', '/api/v1/accounts')

    def place_order(self, symbol, side, type, price=None, size=None):
        data = {'side': side, 'type': type, 'symbol': symbol}
        if price:
            data['price'] = price
        if size:
            data['size'] = size
        return self._make_request('POST', '/api/v1/orders', data=data)

    def cancel_order(self, order_id):
        return self._make_request('DELETE', '/api/v1/orders/{}'.format(order_id))
