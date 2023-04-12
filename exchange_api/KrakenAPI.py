import requests
import hmac
import hashlib
import time
import krakenex

class KrakenAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = krakenex.API(key=self.api_key, secret=self.api_secret)

    def get_ticker(self, symbol):
        response = self.client.query_public('Ticker', {'pair': symbol})
        if 'result' in response:
            result = response['result']
            if symbol in result:
                return float(result[symbol]['c'][0])
        return None

    def get_balance(self):
        response = self.client.query_private('Balance')
        if 'result' in response:
            result = response['result']
            return {currency: float(result[currency]) for currency in result}
        return None

    def create_order(self, symbol, side, quantity, price, order_type='limit'):
        kraken_symbol = symbol.replace('/', '')
        kraken_side = 'buy' if side == 'buy' else 'sell'
        kraken_order_type = 'limit' if order_type == 'limit' else 'market'
        response = self.client.query_private('AddOrder', {
            'pair': kraken_symbol,
            'type': kraken_side,
            'ordertype': kraken_order_type,
            'price': price,
            'volume': quantity
        })
        if 'result' in response:
            result = response['result']
            if 'txid' in result:
                return result['txid'][0]
        return None

    def cancel_order(self, order_id):
        response = self.client.query_private('CancelOrder', {'txid': order_id})
        if 'result' in response:
            result = response['result']
            if 'count' in result and result['count'] == 1:
                return True
        return False

    def get_order_status(self, order_id):
        response = self.client.query_private('QueryOrders', {'txid': order_id})
        if 'result' in response:
            result = response['result']
            if order_id in result['open']:
                return 'open'
            elif order_id in result['closed']:
                return 'closed'
            elif order_id in result['canceled']:
                return 'canceled'
        return None
Note that in this example, we're using the krakenex library to interact with the Kraken API. The KrakenAPI class defines methods to retrieve ticker data, account balances, create and cancel orders, and check order status. These methods map to the corresponding API endpoints provided by Kraken.