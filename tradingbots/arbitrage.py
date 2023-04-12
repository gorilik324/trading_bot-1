import configparser
import json
import logging
import random
import requests
import pandas as pd
from analyzers import OrderBookAnalyzer, TradingPair
from exchange_api import (
    BinanceAPI, Bit2cAPI, BitBayAPI, BitfinexAPI, BitmediaAPI, BitmexAPI, BitsoAPI, BittrexAPI, BTCCAPI, CCEXAPI,
    CexioAPI, ChangellyAPI, ChangeNowAPI, CoinbaseAuth, CoinDCXAPI, CriptoIntercambioAPI, CryptoComTaxAPI, CryptomatAPI,
    CryptopiaAPI, CryptoTraderAPI, CryptoViewAPI, EToroAPI, FBSAPI, FTXAPI, GateIOAPI, GeminiAPI, HitBTCAPI, HuobiAPI,
    KrakenAPI, KuCoinAPI, LiquidAPI, LocalBitcoinsAPI, LunoAPI, NiceHashAPI, OkcoinAPI, OKXAPI, PaybisAPI, PoloniexAPI,
    TaxBitAPI, TheRockTradingAPI, TrustWalletAPI, UpholdAPI, WEXAPI, YoBitAPI
)
import threading

# Define the list of exchanges
exchanges = ['BinanceAPI', 'Bit2cAPI', 'BitBayAPI', 'BitfinexAPI', 'BitmediaAPI', 'BitmexAPI', 'BitsoAPI',
             'BittrexAPI', 'BTCCAPI', 'CCEXAPI', 'CexioAPI', 'ChangellyAPI', 'ChangeNowAPI', 'CoinbaseAuth',
             'CoinDCXAPI', 'CriptoIntercambioAPI', 'CryptoComTaxAPI', 'CryptomatAPI', 'CryptopiaAPI',
             'CryptoTraderAPI', 'CryptoViewAPI', 'EToroAPI', 'FBSAPI', 'FTXAPI', 'GateIOAPI', 'GeminiAPI', 'HitBTCAPI',
             'HuobiAPI', 'KrakenAPI', 'KuCoinAPI', 'LiquidAPI', 'LocalBitcoinsAPI', 'LunoAPI', 'NiceHashAPI',
             'OkcoinAPI', 'OKXAPI', 'PaybisAPI', 'PoloniexAPI', 'TaxBitAPI', 'TheRockTradingAPI', 'TrustWalletAPI',
             'UpholdAPI', 'WEXAPI', 'YoBitAPI']

# Define a lock for thread synchronization
lock = threading.Lock()

# Function to check exchange configuration
def check_exchange_config(config):
    for exchange in exchanges:
        if exchange not in config:
            logging.error(f"No configuration found for {exchange}")

        if 'api_key' not in config[exchange] or 'secret_key' not in config[exchange]:
            logging.error(f"API key or secret key not found in configuration for {exchange}")


class ArbitrageStrategy:
    def __init__(self, trading_pair):
        self.trading_pair = trading_pair

    # Define a thread-safe function to select an exchange
    def select_exchange(self, available_exchanges):
        with lock:
            # Randomly select an exchange from the available exchanges
            return random.choice(available_exchanges)

    # Define a thread-safe function to run the arbitrage
    def run_arbitrage(self):
        # Load configuration from file
        config = configparser.ConfigParser()
        config.read('config.ini')

        # Check exchange configuration
        check_exchange_config(config)

        # Create instances of exchange APIs
        exchange_api_map = {
            'BinanceAPI': BinanceAPI,
            'Bit2cAPI': Bit2cAPI,
            'BitBayAPI': BitBayAPI,
			'BitfinexAPI': BitfinexAPI,
			'BitmediaAPI': BitmediaAPI,
			'BitmexAPI': BitmexAPI,
			'BitsoAPI': BitsoAPI,
			'BittrexAPI': BittrexAPI,
			'BTCCAPI': BTCCAPI,
			'CCEXAPI': CCEXAPI,
			'CexioAPI': CexioAPI,
			'ChangellyAPI': ChangellyAPI,
			'ChangeNowAPI': ChangeNowAPI,
			'CoinbaseAuth': CoinbaseAuth,
			'CoinDCXAPI': CoinDCXAPI,
			'CriptoIntercambioAPI': CriptoIntercambioAPI,
			'CryptoComTaxAPI': CryptoComTaxAPI,
			'CryptomatAPI': CryptomatAPI,
			'CryptopiaAPI': CryptopiaAPI,
			'CryptoTraderAPI': CryptoTraderAPI,
			'CryptoViewAPI': CryptoViewAPI,
			'EToroAPI': EToroAPI,
			'FBSAPI': FBSAPI,
			'FTXAPI': FTXAPI,
			'GateIOAPI': GateIOAPI,
			'GeminiAPI': GeminiAPI,
			'HitBTCAPI': HitBTCAPI,
			'HuobiAPI': HuobiAPI,
			'KrakenAPI': KrakenAPI,
			'KuCoinAPI': KuCoinAPI,
			'LiquidAPI': LiquidAPI,
			'LocalBitcoinsAPI': LocalBitcoinsAPI,
			'LunoAPI': LunoAPI,
			'NiceHashAPI': NiceHashAPI,
			'OkcoinAPI': OkcoinAPI,
			'OKXAPI': OKXAPI,
			'PaybisAPI': PaybisAPI,
			'PoloniexAPI': PoloniexAPI,
			'TaxBitAPI': TaxBitAPI,
			'TheRockTradingAPI': TheRockTradingAPI,
			'TrustWalletAPI': TrustWalletAPI,
			'UpholdAPI': UpholdAPI,
			'WEXAPI': WEXAPI,
			'YoBitAPI': YoBitAPI
			}
           
# Initialize order book analyzer
analyzer = OrderBookAnalyzer()

while True:
    # Get current order book for the selected trading pair from all exchanges
    order_books = {}
    for exchange in exchanges:
        try:
            api_key = config[exchange]['api_key']
            secret_key = config[exchange]['secret_key']
            api = exchange_api_map[exchange](api_key, secret_key)
            order_book = api.get_order_book(self.trading_pair)
            order_books[exchange] = order_book
        except Exception as e:
            logging.error(f"Failed to get order book from {exchange}: {e}")

    # Analyze order books
    analysis = analyzer.analyze(order_books)

    # Perform arbitrage if profitable opportunity found
    if analysis['profitable']:
        logging.info("Profitable arbitrage opportunity found!")
        logging.info(f"Buy on {analysis['buy_exchange']} at {analysis['buy_price']} and sell on {analysis['sell_exchange']} at {analysis['sell_price']}")
        # Implement arbitrage logic here

    # Sleep for a while before checking again
    time.sleep(10)

def __init__(self):
    # Initialize order book analyzer
    self.analyzer = OrderBookAnalyzer()
    # Create a lock for thread synchronization
    self.lock = threading.Lock()

def fetch_order_book(self, exchange, api_key, secret_key):
    try:
        api = exchange_api_map[exchange](api_key, secret_key)
        order_book = api.get_order_book(self.trading_pair)
        with self.lock:
            self.order_books[exchange] = order_book
    except Exception as e:
        logging.error(f"Failed to get order book from {exchange}: {e}")

def start(self):
    # Create threads for fetching order books from exchanges concurrently
    threads = []
    for exchange in exchanges:
        api_key = config[exchange]['api_key']
        secret_key = config[exchange]['secret_key']
        thread = threading.Thread(target=self.fetch_order_book, args=(exchange, api_key, secret_key))
        threads.append(thread)
        thread.start()

    while True:
        # Analyze order books
        analysis = self.analyzer.analyze(self.order_books)

        # Perform arbitrage if profitable opportunity found
        if analysis['profitable']:
            logging.info("Profitable arbitrage opportunity found!")
            logging.info(f"Buy on {analysis['buy_exchange']} at {analysis['buy_price']} and sell on {analysis['sell_exchange']} at {analysis['sell_price']}")
            # Implement arbitrage logic here

        # Sleep for a while before checking again
        time.sleep(10)


In this modified version, we create threads for fetching order books from different exchanges concurrently using the `threading.Thread` class. The `fetch_order_book` method is called as the target function for each thread, and it fetches the order book from the respective exchange's API and stores it in the `order_books` dictionary with a lock to ensure thread safety. The `start` method is modified to loop through the order books and perform analysis, as well as implement arbitrage logic if profitable opportunity is found.

# Update the execute_arbitrage() method of ArbitrageStrategy class
def execute_arbitrage(self, opportunities):
    """
    Execute arbitrage trades for the identified opportunities
    """
    for opportunity in opportunities:
        exchange1 = opportunity['Exchange1']
        exchange2 = opportunity['Exchange2']
        spread_percentage1 = opportunity['SpreadPercentage1']
        spread_percentage2 =opportunity['SpreadPercentage2']
total_spread_percentage = opportunity['TotalSpreadPercentage']
logging.info(f"Arbitrage opportunity found: Exchange1={exchange1}, Exchange2={exchange2}, "
f"SpreadPercentage1={spread_percentage1:.2f}%, SpreadPercentage2={spread_percentage2:.2f}%, "
f"TotalSpreadPercentage={total_spread_percentage:.2f}%")

python
Copy code
        # Execute the arbitrage trade if the total spread percentage is greater than a threshold
        if total_spread_percentage > self.arbitrage_threshold:
            logging.info("Executing arbitrage trade...")

            # Fetch the order books again to get the latest data
            order_books = self.fetch_order_books()

            # Get the best bid and ask prices for both exchanges
            best_bid1 = float(order_books[exchange1]['bids'][0][0])
            best_ask1 = float(order_books[exchange1]['asks'][0][0])
            best_bid2 = float(order_books[exchange2]['bids'][0][0])
            best_ask2 = float(order_books[exchange2]['asks'][0][0])

            # Calculate the amount to trade
            trade_amount = min(best_bid1 * self.trade_percentage, best_bid2 * self.trade_percentage)

            # Execute the buy and sell orders on both exchanges
            buy_order1 = self.execute_order(exchange1, 'buy', trade_amount, best_ask1)
            sell_order2 = self.execute_order(exchange2, 'sell', trade_amount, best_bid2)

            # Calculate the profit
            buy_cost1 = buy_order1['price'] * buy_order1['filled']
            sell_cost2 = sell_order2['price'] * sell_order2['filled']
            profit = sell_cost2 - buy_cost1

            logging.info(f"Arbitrage trade executed: Exchange1={exchange1}, Exchange2={exchange2}, "
                         f"TradeAmount={trade_amount:.2f}, Profit={profit:.2f}")

def execute_order(self, exchange_name, side, amount, price):
    """
    Execute a buy or sell order on the specified exchange
    """
    exchange_api = self.exchange_api_map[exchange_name]
    config_section = exchange_name.lower()
    api_key = config[config_section]['api_key']
    secret_key = config[config_section]['secret_key']
    exchange_instance = exchange_api(api_key, secret_key)
    order = exchange_instance.create_order(self.trading_pair, 'limit', side, amount, price)
    return order

def run(self):
    """
    Run the arbitrage bot
    """
    logging.info("Arbitrage bot started...")
    while True:
        # Fetch order books
        order_books = self.fetch_order_books()

        # Find arbitrage opportunities
        opportunities = self.find_arbitrage_opportunities(order_books)

        # Execute arbitrage trades
        self.execute_arbitrage(opportunities)

        # Sleep for the specified interval before running again
        time.sleep(self.interval)
		
		
if name == 'main':
# Instantiate the arbitrage bot with the desired trading pair and other settings
trading_pair = 'BTC/ETH'
arbitrage_threshold = 5.0
trade_percentage = 0.5
interval = 10
bot = ArbitrageBot(trading_pair, arbitrage_threshold, trade_percentage, interval)

bash
Copy code
# Run the arbitrage bot
bot.run()