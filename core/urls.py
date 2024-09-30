from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.login_user, name='login'),  # Reference your login_user function here
path('register_user/', views.register_user, name='register_user'),
path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_user, name='logout'),
path('save_restaurant/<str:place_id>/', views.save_restaurant, name='save_restaurant'),
    path('saved_restaurants/', views.saved_restaurants, name='saved_restaurants'),

]