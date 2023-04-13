from django.urls import path
from .views import login_view, start_bot_view, stop_bot_view

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('start-bot/', views.start_bot_view, name='start_bot'),
    path('stop-bot/', views.stop_bot_view, name='stop_bot'),
    # Add additional URLs for any other views that you may have
    # Example: path('some-view/', views.some_view, name='some_view'),
]
