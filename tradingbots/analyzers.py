import requests
import json

class OrderBookAnalyzer:
    def __init__(self, exchange_api, trading_pair):
        self.exchange_api = exchange_api
        self.trading_pair = trading_pair

    def get_order_book(self):
        """
        Retrieve the order book for the trading pair from the exchange API.
        """
        order_book = self.exchange_api.get_order_book(self.trading_pair)
        return order_book

    def get_optimal_price(self, order_book, trade_type, trade_amount):
        """
        Analyze the order book to identify the optimal price for executing the trade.
        """
        if trade_type == "buy":
            asks = order_book["asks"]
            cumulative_amount = 0
            for ask in asks:
                cumulative_amount += ask[1]
                if cumulative_amount >= trade_amount:
                    return ask[0]
        elif trade_type == "sell":
            bids = order_book["bids"]
            cumulative_amount = 0
            for bid in bids:
                cumulative_amount += bid[1]
                if cumulative_amount >= trade_amount:
                    return bid[0]
        return None


class SentimentAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key

    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of a given text using a third-party API.
        """
        url = f'https://app.slack.com/client/T0531MCQ21K/C053UBT9WNL?source=browser'
        response = requests.get(url)
        sentiment_data = response.json()
        return sentiment_data['sentiment']

    def get_news_sentiment(self, query):
        """
        Retrieve news articles related to a given query and analyze the sentiment of the articles.
        """
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={self.api_key}"
        response = requests.get(url)
        data = json.loads(response.text)
        articles = data["articles"]
        sentiment_scores = []
        for article in articles:
            title = article["title"]
            description = article["description"]
            text = title + ". " + description
            score = self.analyze_sentiment(text)
            sentiment_scores.append(score)
        return sum(sentiment_scores) / len(sentiment_scores)
