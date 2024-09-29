# users/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .users import HARD_CODED_USERS

@login_required
def user_profile(request):
    user_email = request.user.email
    role = HARD_CODED_USERS.get(user_email, 'unknown')  # Default to 'unknown'
    return render(request, 'users/user_profile.html', {'email': user_email, 'role': role})
