import requests
import time
import hashlib
import hmac
import json

class BitfinexAPI:
    API_URL = "https://api.bitfinex.com/v1"

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def _request(self, method, endpoint, params=None):
        url = self.API_URL + endpoint

        if params is None:
            params = {}

        payload = {
            'request': endpoint,
            'nonce': str(int(time.time() * 1000))
        }
        payload.update(params)

        payload_string = json.dumps(payload)
        payload_encoded = payload_string.encode()
        sig = hmac.new(self.api_secret.encode(), payload_encoded, hashlib.sha384).hexdigest()

        headers = {
            'X-BFX-APIKEY': self.api_key,
            'X-BFX-PAYLOAD': payload_encoded,
            'X-BFX-SIGNATURE': sig
        }

        response = requests.request(method, url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Bitfinex API error: " + response.text)

    def get_ticker(self, symbol):
        endpoint = f"/pubticker/{symbol}"
        return self._request("GET", endpoint)

    def get_order_book(self, symbol, limit=100):
        endpoint = f"/book/{symbol}"
        params = {'limit_bids': limit, 'limit_asks': limit}
        return self._request("GET", endpoint, params=params)

    def create_order(self, symbol, amount, price, side, order_type):
        endpoint = "/order/new"
        params = {
            'symbol': symbol,
            'amount': str(amount),
            'price': str(price),
            'side': side,
            'type': order_type
        }
        return self._request("POST", endpoint, params=params)

    def cancel_order(self, order_id):
        endpoint = f"/order/cancel"
        params = {'order_id': order_id}
        return self._request("POST", endpoint, params=params)

This BitfinexAPI class defines methods for interacting with the Bitfinex exchange API, such as get_ticker, get_order_book, create_order, and cancel_order.

The _request method is a helper method that handles the creation of the authentication headers required by the Bitfinex API. The other methods use the _request method to make API requests and return the response as a Python dictionary.

To use this API class, you would first need to obtain an API key and secret from the Bitfinex exchange, and then create an instance of the BitfinexAPI class with your API key and secret:

python
Copy code
api_key = "your_api_key"
api_secret = "your_api_secret"
api = BitfinexAPI(api_key, api_secret)
You can then use the methods of the BitfinexAPI class to interact with the Bitfinex exchange API, for example:

python
Copy code
ticker = api.get_ticker('btcusd')
order_book = api.get_order_book('btcusd')
order = api.create_order('btcusd', 0.01, 50000, 'buy', 'limit')
api.cancel_order(order['order_id'])