import requests
import json
from .models import TradingPair, Trade

class ArbitrageStrategy:
    def __init__(self, trading_pair, stop_loss=None, time_limit=None, volatility=None, tolerance=None, slippage=None):
        self.trading_pair = trading_pair
        self.stop_loss = stop_loss
        self.time_limit = time_limit
        self.volatility = volatility
        self.tolerance = tolerance
        self.slippage = slippage

    def get_market_data(self, exchange):
        url = f'https://api.{exchange}.com/market-data/{self.trading_pair.name}'
        response = requests.get(url)
        market_data = json.loads(response.content)
        return market_data

    def execute_trade(self, exchange, trade_size, trade_type):
        url = f'https://api.{exchange}.com/trade'
        data = {
            'trading_pair': self.trading_pair.name,
            'size': trade_size,
            'type': trade_type
        }
        response = requests.post(url, data=data)
        trade = Trade.objects.create(
            trading_pair=self.trading_pair,
            user=self.request.user,
            exchange=exchange,
            trade_size=trade_size,
            trade_type=trade_type
        )
        return trade

    def check_stop_loss(self, exchange):
        if self.stop_loss:
            market_data = self.get_market_data(exchange)
            last_price = market_data['last_price']
            if last_price <= self.stop_loss:
                return True
        return False

    def check_time_limit(self, start_time, time_limit_minutes):
        if self.time_limit:
            elapsed_time = (datetime.now() - start_time).total_seconds() / 60
            if elapsed_time >= time_limit_minutes:
                return True
        return False

    def check_volatility(self, market_data):
        if self.volatility:
            last_price = market_data['last_price']
            prev_price = market_data['prev_price']
            if abs(last_price - prev_price) >= self.volatility:
                return True
        return False

    def check_tolerance(self, market_data, buy_exchange, sell_exchange):
        if self.tolerance:
            buy_price = market_data[f'{buy_exchange}_price']
            sell_price = market_data[f'{sell_exchange}_price']
            if abs(buy_price - sell_price) >= self.tolerance:
                return True
        return False

    def check_slippage(self, buy_exchange, sell_exchange):
        if self.slippage:
            buy_order_book = self.get_order_book(buy_exchange)
            sell_order_book = self.get_order_book(sell_exchange)
            buy_price = buy_order_book['bids'][0]['price']
            sell_price = sell_order_book['asks'][0]['price']
            if abs(buy_price - sell_price) >= self.slippage:
                return True
        return False

    def get_order_book(self, exchange):
        url = f'https://api.{exchange}.com/order-book/{self.trading_pair.name}'
        response = requests.get(url)
        order_book = json.loads(response.content)
        return order_book

    def run_arbitrage(self, buy_exchange, sell_exchange, trade_size, trade_type):
        start_time = datetime.now()
        while True:
            if self.check_stop_loss(sell_exchange):
                print(f'Stop loss triggered on {sell_exchange} - exiting trade.')
                return