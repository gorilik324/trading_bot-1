from django.urls import path
from .views import HomePageView, CustomLoginView, CustomLogoutView, CustomPasswordResetView, register_view, login_view, logout_view

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('register/', register_view, name='register'),
]
