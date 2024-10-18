from django.test import TestCase, Client
from django.urls import reverse

# test was working when there existed a url path to team handbook

# class LandingTests(TestCase):
#     def test_redirect_to_team_handbook(self):
#         response = self.client.get(reverse('team_handbook'), follow=True)

#         self.assertEqual(response.status_code, 200)