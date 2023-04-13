import requests
from requests.auth import AuthBase

class CoinbaseAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
    
    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()
        request.headers.update({
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

class CoinbaseAPI:
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.auth = CoinbaseAuth(api_key, secret_key, passphrase)
        self.base_url = 'https://api.coinbase.com/v2/'
        
    def get_balance(self, currency):
        url = f"{self.base_url}accounts"
        response = requests.get(url, auth=self.auth)
        if response.status_code == 200:
            accounts = response.json()['data']
            for account in accounts:
                if account['currency'] == currency:
                    balance = float(account['balance']['amount'])
                    return balance
        return None
    
    def place_order(self, order):
        url = f"{self.base_url}orders"
        response = requests.post(url, json=order, auth=self.auth)
        if response.status_code == 200:
            return response.json()['id']
        return None

This example shows how to create an API class for Coinbase that handles authentication using the Coinbase API key, secret key, and passphrase. The class provides two methods, get_balance and place_order, that allow you to get the balance of a specific currency and place an order, respectively. The get_balance method retrieves the account balances and returns the balance of the specified currency, while the place_order method places an order using the specified parameters.