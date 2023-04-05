from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('start-bot/', views.start_bot_view, name='start_bot'),
    path('stop-bot/', views.stop_bot_view, name='stop_bot'),
]
