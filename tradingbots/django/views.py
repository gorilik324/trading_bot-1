from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.db import transaction  # Import Django's transaction module
from .forms import UserRegisterForm, ExchangeForm, TradeForm
from .models import TradingPair, Trade, Exchange, MarketData, ExchangeCredentials
from tradingbots import arbitrage  # Import the ArbitrageBot class from your module
from tradingbots import strategies
import threading


class CustomLoginView(LoginView):
    template_name = 'tradingbots/django/templates/login.html'

    def login_view(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page after successful login
            else:
                # Handle invalid login credentials
                return render(request, 'login.html', {'error': 'Invalid username or password'})
        else:
            return render(request, 'tradingbots/django/templates/login.html')


    def register(request):
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Your account has been created! You are now able to log in')
                return redirect('login')
        else:
            form = UserRegisterForm()
        return render(request, 'authentication/templates/registration/register.html', {'form': form})


class TradingPairListView(ListView):
    model = TradingPair
    template_name = 'django/pair_list.html'
    context_object_name = 'pairs'


class TradeListView(ListView):
    model = Trade
    template_name = 'django/trade_list.html'
    context_object_name = 'trades'


class ExchangeListView(ListView):
    model = Exchange
    template_name = 'django/exchange_list.html'
    context_object_name = 'exchanges'


class MarketDataListView(ListView):
    model = MarketData
    template_name = 'django/market_data_list.html'
    context_object_name = 'market_data'


class ExchangeCreateView(CreateView):
    model = Exchange
    form_class = ExchangeForm
    template_name = 'django/exchange_create.html'
    success_url = reverse_lazy('exchange_list')


class ExchangeUpdateView(UpdateView):
    model = Exchange
    form_class = ExchangeForm
    template_name = 'django/exchange_update.html'
    success_url = reverse_lazy('exchange_list')


class TradeCreateView(CreateView):
    model = Trade
    form_class = TradeForm
    template_name = 'django/trade_create.html'
    success_url = reverse_lazy('trade_list')


class TradeUpdateView(UpdateView):
    model = Trade
    form_class = TradeForm
    template_name = 'django/trade_update.html'
    success_url = reverse_lazy('trade_list')


# Define thread-safe data structures
market_data_list = []
market_data_lock = threading.Lock()


@transaction.atomic
def perform_arbitrage(request):
    if request.method == 'POST':
        # Assuming you have a form to select buy_exchange and sell_exchange
        buy_exchange = request.POST.get('buy_exchange')
        sell_exchange = request.POST.get('sell_exchange')

        # Create an instance of the ArbitrageBot
        bot = arbitrage.ArbitrageBot()

        # Fetch exchange credentials for buy_exchange and sell_exchange
        buy_exchange_credentials = ExchangeCredentials.objects.get(exchange=buy_exchange)
        sell_exchange_credentials = ExchangeCredentials.objects.get(exchange=sell_exchange)

        # Fetch market data for the selected trading pair
        trading_pair = TradingPair.objects.get(id=request.POST.get('trading_pair'))

        # Fetch market data for buy_exchange and sell_exchange
        buy_market_data = MarketData.objects.get(exchange=buy_exchange, trading_pair=trading_pair)
        sell_market_data = MarketData.objects.get(exchange=sell_exchange, trading_pair=trading_pair)

        # Lock market_data_list to prevent concurrent access
        with market_data_lock:
            # Append market data to market_data_list
            market_data_list.append(buy_market_data)
            market_data_list.append(sell_market_data)

            # Call the arbitrage strategy
            strategy = strategies.SimpleArbitrageStrategy()  # Replace with your desired strategy
            bot.execute_strategy(strategy, market_data_list)

            # Clear market_data_list after execution
            market_data_list.clear()

        # Perform arbitrage trade using the selected exchanges
        bot.perform_arbitrage(buy_exchange_credentials, sell_exchange_credentials, trading_pair)

        # Redirect to the trade list page after successful arbitrage trade
        messages.success(request, 'Arbitrage trade successfully executed!')
        return redirect('trade_list')
    else:
        # Render the perform_arbitrage.html template with necessary data
        exchanges = Exchange.objects.all()
        trading_pairs = TradingPair.objects.all()
        return render(request, 'django/perform_arbitrage.html', {'exchanges': exchanges, 'trading_pairs': trading_pairs})

