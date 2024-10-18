from django.test import TestCase, Client
from django.urls import reverse

class LandingTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_redirect_to_team_handbook(self):
        response = self.client.get(reverse('team_handbook'), follow=True)

        self.assertEqual(response.status_code, 200)