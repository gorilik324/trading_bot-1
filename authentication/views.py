import logging
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from trading_bot.settings import DATABASES
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import User
from .forms import LoginForm, RegistrationForm
# import other necessary modules here


logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    template_name = 'trading_bot/authentication/templates/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'trading_bot/authentication/templates/registration/logout.html'

class CustomPasswordResetView(PasswordResetView):
    template_name = 'trading_bot/authentication/templates/registration/password_reset.html'  # Update the template name

class HomePageView(TemplateView):
    template_name = 'templates/home.html'

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Failed to authenticate user.')
                logger.error(f"Failed to authenticate user {username}.")
        else:
            messages.error(request, 'Invalid form data.')
            logger.error(f"Invalid form data for user {username}. Form data: {form.errors}")
    else:
        form = UserCreationForm()
    return render(request, 'trading_bot/authentication/templates/registration/register.html'), {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            logger.error(f"Failed login attempt for user {username}.")
    return render(request, 'trading_bot/authentication/templates/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'trading_bot/authentication/templates/logout.html')

