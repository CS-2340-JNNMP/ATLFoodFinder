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

def saved_restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'core/profile.html', {'restaurants': restaurants})


def save_restaurant(request, place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={'AIzaSyB6pe7uiKQcdWfmgNBd4ufDu2elm-P_YAQ'}"

    response = requests.get(url)
    details = response.json().get('result', {})

    # Assuming you have a Restaurant model
    Restaurant.objects.create(
        name=details.get('name'),
        address=details.get('formatted_address'),
        rating=details.get('rating'),
        place_id=details.get('place_id'),
    )

    return redirect('saved_restaurants')