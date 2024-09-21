from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.login_user, name='login'),  # Reference your login_user function here
path('register_user/', views.register_user, name='register_user'),

]