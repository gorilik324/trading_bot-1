import requests
import hmac
import hashlib
import time

class LocalBitcoinsAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://localbitcoins.com/api/'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, endpoint, params):
        nonce = int(time.time())
        message = str(nonce) + self.api_key + endpoint + requests.compat.urlencode(sorted(params.items()))
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
        return {'Apiauth-Key': self.api_key, 'Apiauth-Nonce': str(nonce), 'Apiauth-Signature': signature}

    def _make_request(self, method, endpoint, params=None):
        url = self.base_url + endpoint
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        if params:
            headers.update(self._sign_request(endpoint, params))
        response = requests.request(method, url, headers=headers, data=params)
        response.raise_for_status()
        return response.json()

    def get_ticker(self, symbol):
        endpoint = f'/bitcoinaverage/ticker-all-currencies/'
        response = self._make_request('GET', endpoint)
        return response[symbol]

    def get_account_info(self):
        endpoint = '/myself/'
        return self._make_request('GET', endpoint)

    def place_ad(self, ad_type, amount, price, currency='USD'):
        endpoint = '/api/ad-create/'
        params = {'ad_type': ad_type, 'currency': currency, 'margin': price, 'price_equation': f'{price}/btc', 'volume': amount}
        return self._make_request('POST', endpoint, params=params)

    def get_ads(self, currency='USD'):
        endpoint = f'/ads/?currency={currency}'
        return self._make_request('GET', endpoint)

    def get_trades(self):
        endpoint = '/dashboard/'
        return self._make_request('GET', endpoint)
