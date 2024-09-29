from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages

# Define a simple list of users and roles
USER_ROLES = {
    'ncq9fn@virginia.edu': 'admin',
    'user2@example.com': 'common_user',
}


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if email in USER_ROLES:
            user = User(username=email)  # Create a user object
            auth_login(request, user)  # Log the user in
            role = USER_ROLES[email]
            messages.success(request, f'You are logged in as {email}, with role: {role}')
            return redirect('landing:landing_page')  # Adjust this to your landing page URL
        else:
            messages.error(request, 'Invalid email. Please try again.')

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('landing_page')  # Redirect to the landing page after logout
