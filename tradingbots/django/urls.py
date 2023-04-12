from django.urls import path
from .views import TradingPairListView, TradeListView, ExchangeListView, MarketDataListView, ExchangeCreateView, ExchangeUpdateView, TradeCreateView, TradeUpdateView, ExchangeCredentialsCreateView, register, strategies, strategy_result
urlpatterns = [    
    path('login/', views.login_view, name='login'),
    path('register/', register, name='register'),
    path('pairs/', TradingPairListView.as_view(), name='pair_list'),
    path('trades/', TradeListView.as_view(), name='trade_list'),
    path('exchanges/', ExchangeListView.as_view(), name='exchange_list'),
    path('market-data/', MarketDataListView.as_view(), name='market_data_list'),
    path('exchange/create/', ExchangeCreateView.as_view(), name='exchange_create'),
    path('exchange/<int:pk>/update/', ExchangeUpdateView.as_view(), name='exchange_update'),
    path('trade/create/', TradeCreateView.as_view(), name='trade_create'),
    path('trade/<int:pk>/update/', TradeUpdateView.as_view(), name='trade_update'),
    # Update the path for TradeListView and TradeCreateView to include the 'TradingPair' and 'Exchange' models
    path('trades/<int:trading_pair_id>/<int:exchange_id>/', TradeListView.as_view(), name='trade-list'),
    path('trades/<int:trading_pair_id>/<int:exchange_id>/create/', TradeCreateView.as_view(), name='trade-create'),
    # Add URLs for other views related to models such as TradingPairListView, ExchangeListView, etc.
    path('trading-pairs/', TradingPairListView.as_view(), name='trading-pair-list'),
    path('market-data/<int:trading_pair_id>/<int:exchange_id>/', MarketDataListView.as_view(), name='market-data-list'),
    path('exchange-credentials/<int:exchange_id>/', ExchangeCredentialsCreateView.as_view(), name='exchange-credentials-create'),
    path('strategies/', strategies, name='strategies'),
    path('strategy_result/', strategy_result, name='strategy_result'),
]
