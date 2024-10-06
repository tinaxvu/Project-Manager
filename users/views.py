# users/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def user_profile(request):
    user = request.user
    user_email = user.email
    user_groups = user.groups.all()
    return render(request, 'users/user_profile.html', {'email': user_email, 'groups': user_groups}) 
