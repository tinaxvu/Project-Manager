from django.shortcuts import render


def landing_page(request):
    user_authenticated = request.user.is_authenticated
    user = request.user

    return render(request, 'landing/index.html', {
        'user_authenticated': user_authenticated,
        'user': user,
    })
