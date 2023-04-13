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
from trading_bot.settings import DATABASES
import threading

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

    def convert_to_usdt(self, amount):
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
    response.raise_for_status()
    response_data = response.json()
    # Update the code to send the converted USDT amount to the trust wallet address: TLGcdTwtdoPgUt4iwvrFb2obipbXcvWAxM
    # Update the code to handle the response and send the converted amount to the trust wallet address
    # Update the code to return the converted USDT amount
    usdt_amount = response_data['usdt_amount']
    return usdt_amount
except requests.exceptions.RequestException as e:
    logger.error(f"Failed to convert amount to USDT: {e}")
    raise ValueError("Failed to convert amount to USDT")

def send_to_internal_wallet(self, amount, wallet_address):
# Implement logic to send amount to internal wallet address
# Update the code to handle sending amount to the provided wallet address
# Update the code to handle success and error scenarios
# Update the code to update logging and handle exceptions if necessary
pass

def update_logging_file(self, profit_part_1, profit_part_2):
# Implement logic to update logging file with trade details
# Update the code to handle writing trade details to logging file
# Update the code to handle exceptions if necessary
pass

def save(self, *args, **kwargs):
# Check if the associated TradingPair instance exists and update quantity field
if self.trading_pair and not self.quantity:
self.quantity = self.amount / self.price

super().save(*args, **kwargs)

