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
