from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .forms import UserRegisterForm, ExchangeForm, TradeForm
from .models import TradingPair, Trade, Exchange, MarketData, ExchangeCredentials


class CustomLoginView(LoginView):
    template_name = 'trading_bot/login.html'


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
    return render(request, 'trading_bot/register.html', {'form': form})


class TradingPairListView(ListView):
    model = TradingPair
    template_name = 'trading_bot/pair_list.html'
    context_object_name = 'pairs'


class TradeListView(ListView):
    model = Trade
    template_name = 'trading_bot/trade_list.html'
    context_object_name = 'trades'


class ExchangeListView(ListView):
    model = Exchange
    template_name = 'trading_bot/exchange_list.html'
    context_object_name = 'exchanges'


class MarketDataListView(ListView):
    model = MarketData
    template_name = 'trading_bot/market_data_list.html'
    context_object_name = 'market_data'


class ExchangeCreateView(CreateView):
    model = Exchange
    form_class = ExchangeForm
    template_name = 'trading_bot/exchange_create.html'
    success_url = reverse_lazy('exchange_list')


class ExchangeUpdateView(UpdateView):
    model = Exchange
    form_class = ExchangeForm
    template_name = 'trading_bot/exchange_update.html'
    success_url = reverse_lazy('exchange_list')


class TradeCreateView(CreateView):
    model = Trade
    form_class = TradeForm
    template_name = 'trading_bot/trade_create.html'
    success_url = reverse_lazy('trade_list')


class TradeUpdateView(UpdateView):
    model = Trade
    form_class = TradeForm
    template_name = 'trading_bot/trade_update.html'
    success_url = reverse_lazy('trade_list')
