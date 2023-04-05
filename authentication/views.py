# views.py
import logging

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView

logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    pass

class CustomPasswordResetView(PasswordResetView):
    pass

class HomePageView(TemplateView):
    template_name = 'home.html'

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
    return render(request, 'registration/register.html', {'form': form})

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
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('register/', register_view, name='register'),
]
