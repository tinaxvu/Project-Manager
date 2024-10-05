# landing/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def landing_page(request):
    if request.user.is_authenticated:
        user = request.user
        user_email = user.email  # Get the logged-in user's email
        user_groups = user.groups.all()
        return render(request, 'landing/index.html', {'email': user_email, 'groups': user_groups})
    else:
        return render(request, 'landing/index.html', {'error': 'You are not logged in.'})


