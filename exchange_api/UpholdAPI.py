import requests
import hmac
import hashlib
import time

class UpholdAPI:
    def __init__(self, api_key, secret_key):
        self.base_url = 'https://api.uphold.com'
        self.api_key = api_key
        self.secret_key = secret_key

    def _sign_request(self, method, path, nonce, body=''):
        message = method + path + nonce + body
        signature = hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()
        return signature

    def _make_request(self, method, path, params=None):
        url = self.base_url + path
        nonce = str(int(time.time() * 1000))
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'X-Request-Nonce': nonce,
            'X-Request-Signature': '',
        }
        if params:
            body = json.dumps(params)
        else:
            body = ''
        signature = self._sign_request(method, path, nonce, body)
        headers['X-Request-Signature'] = signature
        response = requests.request(method, url, headers=headers, data=body)
        response.raise_for_status()
        return response.json()

    def get_ticker(self, symbol):
        path = f'/v0/ticker/{symbol}'
        return self._make_request('GET', path)

    def get_accounts(self):
        path = '/v0/me'
        return self._make_request('GET', path)

    def create_card(self, label, currency):
        path = '/v0/me/cards'
        params = {'label': label, 'currency': currency}
        return self._make_request('POST', path, params=params)

    def get_transactions(self, card_id):
        path = f'/v0/me/cards/{card_id}/transactions'
        return self._make_request('GET', path)

    def commit_transaction(self, transaction_id):
        path = f'/v0/me/transactions/{transaction_id}/commit'
        return self._make_request('POST', path)
