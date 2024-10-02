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
            return redirect('profile')


        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'core/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile')

        else:
            form=UserCreationForm()
    else:
        form = UserCreationForm()
    return render(request, 'core/register_user.html', {'form' : form})
def sign_up(request):
    return render(request, "core/sign_up.html")
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'core/profile.html', {'user': request.user})

def contact(request):
    return render(request, "core/contact.html")


import requests
from django.http import JsonResponse
from django.shortcuts import render

# Replace with your own API key
API_KEY = 'AIzaSyB6pe7uiKQcdWfmgNBd4ufDu2elm-P_YAQ'


def search_address(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        if address:
            place_details = get_place_details_by_address(address)
            return JsonResponse(place_details)
        else:
            return JsonResponse({'error': 'No address provided'}, status=400)
    return render(request, 'your_template.html')


def get_place_details_by_address(address):
    endpoint = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        'input': address,
        'inputtype': 'textquery',
        'fields': 'place_id,formatted_address,name,geometry',
        'key': API_KEY
    }

    response = requests.get(endpoint, params=params)
    result = response.json()

    if result['status'] == 'OK' and result['candidates']:
        place = result['candidates'][0]  # Taking the first candidate result
        place_id = place.get('place_id')

        # Fetch more details using place_id if required
        detailed_place_info = get_detailed_place_info(place_id)
        return detailed_place_info
    else:
        return {'error': 'Place not found'}


def get_detailed_place_info(place_id):
    endpoint = f"https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'fields': 'name,rating,formatted_address,business_status,types,website,reviews,photos',
        'key': API_KEY
    }

    response = requests.get(endpoint, params=params)
    place_details = response.json()

    if place_details['status'] == 'OK':
        return place_details['result']
    else:
        return {'error': 'Failed to retrieve place details'}
