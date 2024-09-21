from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def index(request):
    return render(request, "core/index.html")

def map(request):
    return render(request, "core/map.html")

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)  # Redirect to success page
            return redirect('index')

        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'core/login.html', {})

def register_user(request):
    return render(request, 'core/register_user.html', {})
def sign_up(request):
    return render(request, "core/sign_up.html")

def contact(request):
    return render(request, "core/contact.html")