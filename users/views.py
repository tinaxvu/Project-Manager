# users/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .users import HARD_CODED_USERS

@login_required
def user_profile(request):
    # Get the logged-in user's email
    user_email = request.user.email
    # Determine the user's role based on the hardcoded list
    role = HARD_CODED_USERS.get(user_email, 'unknown')  # Default to 'unknown'
    return render(request, 'users/user_profile.html', {'email': user_email, 'role': role})
