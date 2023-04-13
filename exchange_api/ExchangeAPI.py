import requests

class ExchangeAPI:
def  __init__(self, api_key, secret_key):
self.api_key = api_key
self.secret_key = secret_key

def get_price(self, symbol):
    url = f"https://api.example.com/price?symbol={symbol}"
    headers = {"X-MBX-APIKEY": self.api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    if "price" in data:
        return float(data["price"])
    else:
        raise ValueError("Failed to retrieve price from API response.")