from django.contrib.auth.models import User

class UserProfile:
    permissions = (
        ('admin', 'admin'),
        ('common_user', 'common_user'),
    )

    # Hardcoded user data
    USERS = {
        'ncq9fn@virginia.edu': {'username': 'ncq9fn', 'role': 'admin'},
        'user2@gmail.com': {'username': 'user2', 'role': 'common_user'},
        # Add more users as needed
    }

    @classmethod
    def get_user_profile(cls, email):
        return cls.USERS.get(email)

    @classmethod
    def has_permission(cls, email, permission):
        user_profile = cls.get_user_profile(email)
        return user_profile and user_profile['role'] == permission
