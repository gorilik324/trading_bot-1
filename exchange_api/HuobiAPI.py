Sure, here's an example of how to create an API class for the Huobi exchange using the Huobi Python SDK:
import requests
import hmac
import hashlib
import time
import huobi

class HuobiAPI:
    def __init__(self, api_key, secret_key):
        self.client = huobi.HuobiDM(api_key=api_key, secret_key=secret_key)

    def get_symbol_price(self, symbol):
        # Get the latest trade price for a symbol
        response = self.client.get_contract_trade(symbol=symbol)
        if response['status'] == 'error':
            raise Exception(response['err-msg'])
        price = response['data'][0]['trade_price']
        return price

    def place_order(self, symbol, direction, price, quantity):
        # Place an order on the exchange
        contract_type = 'quarter'  # You can set this to 'this_week', 'next_week', or 'quarter'
        offset = 'open'  # You can set this to 'open' or 'close'
        lever_rate = 10  # You can set the leverage level, 10 is the default
        response = self.client.send_contract_order(symbol=symbol, contract_type=contract_type, \
                                                    price=price, volume=quantity, direction=direction, \
                                                    offset=offset, lever_rate=lever_rate)
        if response['status'] == 'error':
            raise Exception(response['err-msg'])
        order_id = response['data']['order_id']
        return order_id

    def get_order_status(self, order_id):
        # Get the status of an order on the exchange
        response = self.client.get_contract_order_info(order_id=order_id)
        if response['status'] == 'error':
            raise Exception(response['err-msg'])
        status = response['data'][0]['status']
        return status

    def cancel_order(self, order_id):
        # Cancel an order on the exchange
        response = self.client.cancel_contract_order(order_id=order_id)
        if response['status'] == 'error':
            raise Exception(response['err-msg'])
        return True

    def get_balance(self, symbol):
        # Get the balance of a symbol in your account
        response = self.client.get_contract_account_info(symbol=symbol)
        if response['status'] == 'error':
            raise Exception(response['err-msg'])
        balance = response['data'][0]['margin_available']
        return balance

Note that this example uses the Huobi DM (derivative market) API, which is used for trading futures contracts. If you want to trade on the spot market or use other features of the exchange, you will need to use the Huobi Spot API or the Huobi ECO Chain API, respectively. Also, be sure to follow the Huobi API documentation and guidelines for proper usage of the API.