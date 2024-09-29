from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Redirects to Google login
    path('logout/', views.logout_view, name='logout'),  # Handles logout
]
