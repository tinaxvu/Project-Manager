# landing/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.users import HARD_CODED_USERS


def landing_page(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        user_email = request.user.email  # Get the logged-in user's email
        role = HARD_CODED_USERS.get(user_email, 'unknown')  # Get role or default to 'unknown'
        return render(request, 'landing/index.html', {'email': user_email, 'role': role})

    # If not authenticated, display the message
    return render(request, 'landing/index.html', {'error': 'You are not logged in.'})
