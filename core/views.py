from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "core/index.html")

def map(request):
    return render(request, "core/map.html")

def login(request):
    return render(request, "core/login.html")

def sign_up(request):
    return render(request, "core/sign_up.html")

def contact(request):
    return render(request, "core/contact.html")