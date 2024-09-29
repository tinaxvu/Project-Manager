# users/urls.py

from django.urls import path
from .views import user_profile

app_name = 'users'

urlpatterns = [
    path('profile/', user_profile, name='profile'),
]
