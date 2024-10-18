from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.test.client import Client

class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser@gmail.com', 'password')

    def test_logged_in_user_profile_view(self):
        self.client.login(email='testuser@gmail.com',password='password')
        response = self.client.get(reverse('landing_page'))

        self.assertEqual(response.status_code, 200)
    