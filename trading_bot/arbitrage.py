import requests
import json

class ArbitrageStrategy:
    def __init__(self, trading_pair):
        self.trading_pair = trading_pair

    def get_market_data(self, exchange):
        url = f'https://api.{exchange}.com/market-data/{self.trading_pair.name}'
        response = requests.get(url)
        market_data = json.loads(response.content)
        return market_data

    def execute_trade(self, exchange, trade_size, trade_type, user=None):
    url = f'https://api.{exchange}.com/trade'
    data = {
        'trading_pair': self.trading_pair.name,
        'size': trade_size,
        'type': trade_type
    }
    response = requests.post(url, data=data)
    if user:
        trade = Trade.objects.create(
            trading_pair=self.trading_pair,
            user=user,
            exchange=exchange,
            trade_size=trade_size,
            trade_type=trade_type
        )
    else:
        trade = None
    return trade

    def arbitrage(self, exchange_1, exchange_2, min_profit):
        market_data_1 = self.get_market_data(exchange_1)
        market_data_2 = self.get_market_data(exchange_2)

        # Calculate the best bid/ask prices for each exchange
        best_bid_1 = market_data_1['best_bid']
        best_ask_1 = market_data_1['best_ask']
        best_bid_2 = market_data_2['best_bid']
        best_ask_2 = market_data_2['best_ask']

        # Calculate the potential profit
        profit = (best_bid_2 - best_ask_1) / best_ask_1

        # Check if the potential profit is greater than the minimum profit threshold
        if profit >= min_profit:
            # Execute the trades
            trade_size_1 = min(best_ask_1['size'], best_bid_2['size'])
            trade_size_2 = trade_size_1 * best_ask_1['price']
            self.execute_trade(exchange_1, trade_size_1, 'sell')
            self.execute_trade(exchange_2, trade_size_2, 'buy')
            return f'Trades executed successfully. Potential profit: {profit}'
        else:
            return f'Potential profit ({profit}) is below the minimum threshold ({min_profit}). No trades executed.'
