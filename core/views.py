from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "core/index.html")

def map(request):
    return render(request, "core/map.html")