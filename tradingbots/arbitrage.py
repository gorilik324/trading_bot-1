import configparser
import json
import logging
import random
import threading
import requests
import pandas as pd
from tradingbots.analyzers import OrderBookAnalyzer, TradingPair
from tradingbots.exchange_api import (
    BinanceAPI, Bit2cAPI, BitBayAPI, BitfinexAPI, BitmediaAPI, BitmexAPI, BitsoAPI, BittrexAPI, BTCCAPI, BtCexAPI, BybitAPI, CCEXAPI,
    CexioAPI, ChangellyAPI, ChangeNowAPI, CoinbaseAuth, CoinDCXAPI, CriptoIntercambioAPI, CryptoComTaxAPI, CryptomatAPI,
    CryptopiaAPI, CryptoTraderAPI, CryptoViewAPI, EToroAPI, FBSAPI, FTXAPI, GateIOAPI, GeminiAPI, HitBTCAPI, HuobiAPI,
    KrakenAPI, KuCoinAPI, LiquidAPI, LocalBitcoinsAPI, LunoAPI, NiceHashAPI, OkcoinAPI, OKXAPI, PaybisAPI, PoloniexAPI,
    TaxBitAPI, TheRockTradingAPI, TrustWalletAPI, UpholdAPI, WEXAPI, YoBitAPI
)

Function to check exchange configuration

# Other parts of the code that use the check_exchange_config() function
def check_exchange_config(config):
    Define the list of exchanges
        exchanges = ['BinanceAPI', 'Bit2cAPI', 'BitBayAPI', 'BitfinexAPI', 'BitmediaAPI', 'BitmexAPI', 'BitsoAPI',
    'BittrexAPI', 'BTCCAPI', 'BtCexAPI', 'BybitAPI', 'CCEXAPI', 'CexioAPI', 'ChangellyAPI', 'ChangeNowAPI', 'CoinbaseAuth',
    'CoinDCXAPI', 'CriptoIntercambioAPI', 'CryptoComTaxAPI', 'CryptomatAPI', 'CryptopiaAPI',
    'CryptoTraderAPI', 'CryptoViewAPI', 'EToroAPI', 'FBSAPI', 'FTXAPI', 'GateIOAPI', 'GeminiAPI', 'HitBTCAPI',
    'HuobiAPI', 'KrakenAPI', 'KuCoinAPI', 'LiquidAPI', 'LocalBitcoinsAPI', 'LunoAPI', 'NiceHashAPI',
    'OkcoinAPI', 'OKXAPI', 'PaybisAPI', 'PoloniexAPI', 'TaxBitAPI', 'TheRockTradingAPI', 'TrustWalletAPI',
    'UpholdAPI', 'WEXAPI', 'YoBitAPI']  # Replace with actual exchange names
        for exchange in exchanges:
            if exchange not in config:
                logging.error(f"No configuration found for {exchange}")

            if 'api_key' not in config[exchange] or 'secret_key' not in config[exchange]:
                logging.error(f"API key or secret key not found in configuration for {exchange}")

# Update the __init__() method of ArbitrageStrategy class
class ArbitrageStrategy:
    def __init__(self, trading_pair):
        self.trading_pair = trading_pair
        self.exchange_api_map = {
            'Binance': BinanceAPI,
            'Bit2c': Bit2cAPI,
            'BitBay': BitBayAPI,
            'Bitfinex': BitfinexAPI,
            'Bitmedia': BitmediaAPI,
            'Bitmex': BitmexAPI,
            'Bitso': BitsoAPI,
            'Bittrex': BittrexAPI,
            'BTCC': BTCCAPI,
            'BtCex': BtCexAPI,
            'Bybit': BybitAPI,
            'CCEX': CCEXAPI,
            'Cexio': CexioAPI,
            'Changelly': ChangellyAPI,
            'ChangeNow': ChangeNowAPI,
            'CoinbaseAuth': CoinbaseAuth,
            'CoinDCX': CoinDCXAPI,
            'CriptoIntercambio': CriptoIntercambioAPI,
            'CryptoComTax': CryptoComTaxAPI,
            'Cryptomat': CryptomatAPI,
            'Cryptopia': CryptopiaAPI,
            'CryptoTrader': CryptoTraderAPI,
            'CryptoView': CryptoViewAPI,
            'EToro': EToroAPI,
            'FBS': FBSAPI,
            'FTX': FTXAPI,
            'GateIO': GateIOAPI,
            'Gemini': GeminiAPI,
            'HitBTC': HitBTCAPI,
            'Huobi': HuobiAPI,
            'Kraken': KrakenAPI,
            'KuCoin': KuCoinAPI,
            'Liquid': LiquidAPI,
            'LocalBitcoins': LocalBitcoinsAPI,
            'Luno': LunoAPI,
            'NiceHash': NiceHashAPI,
            'Okcoin': OkcoinAPI,
            'OKX': OKXAPI,
            'Paybis': PaybisAPI,
            'Poloniex': PoloniexAPI,
            'TaxBit': TaxBitAPI,
            'TheRockTrading': TheRockTradingAPI,
            'TrustWallet': TrustWalletAPI,
            'Uphold': UpholdAPI,
            'WEX': WEXAPI,
            'YoBit': YoBitAPI
        }
        
self.order_books_lock = threading.Lock()
self.order_books = {}

    def fetch_order_books(self):
    """
    Fetch order books for the specified trading pair from all available exchanges
    """
    threads = []
    for exchange in self.available_exchanges:
        exchange_api = self.exchange_api_map[exchange]
        config_section = exchange.lower()
        if config_section not in config:
            logging.error(f"No configuration found for {exchange}")
            continue

        if 'api_key' not in config[config_section] or 'secret_key' not in config[config_section]:
            logging.error(f"API key or secret key not found in configuration for {exchange}")
            continue

        api_key = config[config_section]['api_key']
        secret_key = config[config_section]['secret_key']
        api = exchange_api(api_key, secret_key)
        t = threading.Thread(target=self.fetch_order_book, args=(api, exchange))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

def fetch_order_book(self, api, exchange):
    """
    Fetch order book for the specified trading pair from the given exchange API
    """
    try:
        trading_pair = TradingPair(self.trading_pair)
        order_book = api.get_order_book(trading_pair)
        with self.order_books_lock:
            self.order_books[exchange] = order_book
    except Exception as e:
        logging.error(f"Failed to fetch order book for {exchange}: {e}")

# Rest of the code
...

    def find_arbitrage_opportunities(self, order_books):
        """
        Find arbitrage opportunities in the fetched order books
        """
        opportunities = []
        for exchange1 in order_books:
            for exchange2 in order_books:
                if exchange1 != exchange2:
                    order_book1 = order_books[exchange1]
                    order_book2 = order_books[exchange2]
                    trading_pair1 = TradingPair(order_book1['symbol'])
                    trading_pair2 = TradingPair(order_book2['symbol'])
                    if trading_pair1.base_asset == trading_pair2.quote_asset and \
                            trading_pair1.quote_asset == trading_pair2.base_asset:
                    # Perform arbitrage check                    
                    best_bid1 = float(order_book1['bids'][0][0])
                    best_ask1 = float(order_book1['asks'][0][0])
                    best_bid2 = float(order_book2['bids'][0][0])
                    best_ask2 = float(order_book2['asks'][0][0])
                    if best_bid1 > 0 and best_ask1 > 0 and best_bid2 > 0 and best_ask2 > 0:
                        spread1 = best_ask1 - best_bid1
                        spread2 = best_ask2 - best_bid2
                        spread_percentage1 = (spread1 / best_bid1) * 100
                        spread_percentage2 = (spread2 / best_bid2) * 100
                        if spread_percentage1 > 0 and spread_percentage2 > 0:
                            if spread_percentage1 + spread_percentage2 > 100:
                                opportunities.append({
                                    'Exchange1': exchange1,
                                    'Exchange2': exchange2,
                                    'Spread1': spread1,
                                    'Spread2': spread2,
                                    'SpreadPercentage1': spread_percentage1,
                                    'SpreadPercentage2': spread_percentage2,
                                    'TotalSpreadPercentage': spread_percentage1 + spread_percentage2
                                })

    return opportunities

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
    interval = 60
    bot = ArbitrageBot(trading_pair, arbitrage_threshold, trade_percentage, interval)

    bash
    Copy code
    # Run the arbitrage bot
    bot.run()