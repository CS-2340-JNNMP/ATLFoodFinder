from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import Restaurant, SavedRestaurant
import requests
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


class UserCreationFormWrapper(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationFormWrapper, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-styles'})



def register_user(request):
    if request.method == 'POST':
        form = UserCreationFormWrapper(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile')

        else:
            form=UserCreationFormWrapper()
    else:
        form = UserCreationFormWrapper()
    return render(request, 'core/register_user.html', {'form' : form})
def sign_up(request):
    return render(request, "core/sign_up.html")
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'core/profile.html', {'user': request.user})

def contact(request):
    return render(request, "core/contact.html")

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

def search(request):
    return render(request, "core/search.html")
    # views.py


@login_required
@csrf_exempt
def save_restaurant(request, place_id):
    if request.method == 'POST':
        # Retrieve restaurant details from Google Places API

        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key=AIzaSyB6pe7uiKQcdWfmgNBd4ufDu2elm-P_YAQ"
        response = requests.get(url)
        details = response.json().get('result', {})

        photo_reference = details.get('photos', [{}])[0].get('photo_reference') if details.get('photos') else None
        photo_url = None
        if photo_reference:
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key=AIzaSyB6pe7uiKQcdWfmgNBd4ufDu2elm-P_YAQ"

        restaurant, created = Restaurant.objects.get_or_create(
            place_id=details.get('place_id'),
            defaults={
                'image': photo_url,
                'name': details.get('name'),
                'address': details.get('formatted_address'),
                'rating': details.get('rating'),


            }
        )


        SavedRestaurant.objects.get_or_create(user=request.user, restaurant=restaurant)

        return redirect('saved_restaurants')

@login_required
def saved_restaurants(request):
    saved_restaurants = SavedRestaurant.objects.filter(user=request.user)
    return render(request, 'core/savedRestaurant.html', {'saved_restaurants': saved_restaurants})

def unsave_restaurant(request, place_id):
    if request.method == 'POST':
        # Retrieve and delete the saved restaurant
        saved_restaurant = get_object_or_404(SavedRestaurant, restaurant__place_id=place_id)
        saved_restaurant.delete()
        return JsonResponse({'success': True, 'message': 'Restaurant removed successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})
