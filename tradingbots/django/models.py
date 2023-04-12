from django.db import models
import logging
from decimal import Decimal
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import transaction
from django.contrib.auth.models import AbstractUser
import requests
from settings import DATABASES

class CustomUser(AbstractUser):
    pass


class TradingPair(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


DATABASES = DATABASES.settings

logger = logging.getLogger(__name__)

class Trade(models.Model):
    # Define the Trade model

    trading_pair = models.ForeignKey(TradingPair, on_delete=models.CASCADE, related_name='trades')
    exchange = models.ForeignKey('Exchange', on_delete=models.CASCADE, related_name='trades')
    amount = models.DecimalField(max_digits=15, decimal_places=8)
    price = models.DecimalField(max_digits=15, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.FloatField()
    completed = models.BooleanField(default=False)
    profit = models.FloatField(null=True, blank=True)
    usdt_wallet = 'TLGcdTwtdoPgUt4iwvrFb2obipbXcvWAxM'  # Update with your own USDT wallet address
    use_user_area = models.BooleanField(default=False)  # Field to enable/disable user area
    user_area_wallet = models.CharField(max_length=42, null=True, blank=True)

    # Rest of the model code

    def __str__(self):
        return f"{self.trading_pair} trade on {self.exchange} at {self.timestamp}"
        
    def calculate_profit(self):
        # Calculate profit based on trade data and user's balance
        profit = self.quantity * self.price * 0.5
        return profit

    def execute_trade(self):
        # Calculate profit
        profit = self.calculate_profit()

        # Split profit into two parts
        profit_part_1 = profit * 0.5
        profit_part_2 = profit * 0.5

        # Convert profit_part_1 to USDT and send to internal wallet if USDT wallet is provided
        if self.usdt_wallet:
            usdt_amount = self.convert_to_usdt(profit_part_1)
            self.send_to_internal_wallet(usdt_amount, self.usdt_wallet)

        # Update logging file
        self.update_logging_file(profit_part_1, profit_part_2)

        # Update user's balance
        self.user.balance += profit_part_2
        self.user.save()

        # Update trade status
        self.completed = True
        self.profit = profit
        self.save()

    @staticmethod
    @receiver(post_save, sender='Trade')
    def execute_trade(sender, instance, created, **kwargs):
        if created:
            instance.execute_trade()


class Exchange(models.Model):
    name = models.CharField(max_length=50)
    website = models.URLField()
    api_key = models.CharField(max_length=50)
    api_secret = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MarketData(models.Model):
    trading_pair = models.ForeignKey(TradingPair, on_delete=models.CASCADE, related_name='market_data')
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='market_data')
    timestamp = models.DateTimeField(auto_now_add=True)
    bid_price = models.DecimalField(max_digits=15, decimal_places=8)
    ask_price = models.DecimalField(max_digits=15, decimal_places=8)

    def __str__(self):
        return f"{self.trading_pair} market data on {self.exchange} at {self.timestamp}"


class ExchangeCredentials(models.Model):
    ask_price = models.DecimalField(max_digits=15, decimal_places=8)
	exchange = models.OneToOneField(Exchange, on_delete=models.CASCADE, related_name='credentials')
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	api_key = models.CharField(max_length=50)
	api_secret = models.CharField(max_length=50)
	api_passphrase = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Credentials for {self.exchange} of {self.user}"

    def save(self, *args, **kwargs):
        # Check if the associated Exchange instance has a valid API key and secret
        if not self.exchange.api_key or not self.exchange.api_secret:
            raise ValidationError("Exchange API key and secret must be provided before saving credentials.")
        super().save(*args, **kwargs)
        
    def convert_to_usdt(amount):
    # Implement logic to convert amount to USDT using Huobi exchange API
    # Update the code to send the converted USDT amount to the trust wallet address: TLGcdTwtdoPgUt4iwvrFb2obipbXcvWAxM
    
    # Make API request to Huobi exchange to convert amount to USDT
    api_url = "https://api.huobi.com/v1/account/transfer"
    payload = {
        "amount": amount,
        "currency_from": "USD",
        "currency_to": "USDT",
        "address": "TLGcdTwtdoPgUt4iwvrFb2obipbXcvWAxM"
    }
    try:
        response = requests.post(api_url, data=payload)
        response.raise_for_status()  # Raise exception if response has error status code
        # Process the response and return the converted USDT amount
        converted_amount = response.json().get("converted_amount")
        return converted_amount
    except requests.exceptions.RequestException as e:
        # Handle network errors
        raise Exception(f"Failed to convert amount to USDT: {e}") from e
    except (ValueError, KeyError) as e:
        # Handle JSON decoding errors or missing key errors in the response
        raise Exception("Failed to process response from Huobi API") from e
        
    def send_to_internal_wallet(amount, wallet_address):
    # Implement logic to send amount to internal wallet
    # Update the code to use the provided wallet_address: TLGcdTwtdoPgUt4iwvrFb2obipbXcvWAxM
    
     # Make API request to send amount to internal wallet
    api_url = "https://cex.io/api/send"
    payload = {
        "amount": amount,
        "wallet_address": TLGcdTwtdoPgUt4iwvrFb2obipbXcvWAxM
    }
    try:
        response = requests.post(api_url, data=payload)
        response.raise_for_status()  # Raise exception if response has error status code
        # Process the response and return success message
        return "Amount sent to internal wallet successfully"
    except requests.exceptions.RequestException as e:
        # Handle network errors
        raise Exception(f"Failed to send amount to internal wallet: {e}") from e
        
    def update_logging_file(profit_part_1, profit_part_2):
    # Implement logic to update logging file with profit information
    # Update the code to append profit information to a logging file
    
    # Open logging file in append mode and write profit information
    try:
        with open("profit_log.txt", "a") as log_file:
            log_file.write(f"Profit Part 1: {profit_part_1}, Profit Part 2: {profit_part_2}\n")
    except IOError as e:
        # Handle file I/O errors
        raise Exception("Failed to update logging file") from e