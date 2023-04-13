from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class StartBotForm(forms.Form):
    symbol = forms.CharField(label='Symbol', max_length=10)
    quantity = forms.DecimalField(label='Quantity', max_digits=10, decimal_places=2)
    strategy = forms.ChoiceField(label='Strategy', choices=[
        ('mean_reversion', 'Mean Reversion'),
        ('trend_following', 'Trend Following'),
    ])
    stop_loss = forms.DecimalField(label='Stop Loss', max_digits=10, decimal_places=2)
    # Additional fields for the trading bot parameters
    take_profit = forms.DecimalField(label='Take Profit', max_digits=10, decimal_places=2)
    leverage = forms.IntegerField(label='Leverage')
    use_trailing_stop = forms.BooleanField(label='Use Trailing Stop', required=False)
    # Additional fields for the trading bot parameters
    # Add more fields here as needed
