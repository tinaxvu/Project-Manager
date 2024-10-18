from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Project, Todo

# test once database is made

# class ProjectTest(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(username='tester',email='testuser@gmail.com',password='password')
#         self.project = Project.objects.create(name='Test Project', description='Testing description', created_by=self.user)
#     def test_create_todo(self):
#         todo = Todo.objects.create(
#             project=self.project,
#             description='Test todo',
#             date_due='2028-12-01',
#             priority='High',
#             created_by=self.user
#         )
#         self.assertEqual(todo.description, 'Test todo')
#         self.assertFalse(todo.is_finished)
