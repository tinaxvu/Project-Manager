from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Project, Todo, Calendar, ScheduleMeet
from django.urls import reverse


class ProjectTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='tester',email='testuser@gmail.com',password='password')
        self.project = Project.objects.create(name='Test Project',
            description='Testing description', 
            created_by=self.user
            )

    def test_create_project(self):
        self.assertEqual(self.project.name, 'Test Project')
        self.assertEqual(self.project.description, 'Testing description')
        self.assertEqual(self.project.created_by, self.user)

    def test_create_todo(self):
        todo = Todo.objects.create(
            project=self.project,
            description='Test todo',
            date_due='2028-12-01',
            priority='High',
            created_by=self.user
        )
        self.assertEqual(todo.description, 'Test todo')
        self.assertFalse(todo.is_finished)

    def test_create_calendar_event(self):
        event = Calendar.objects.create(
            project=self.project,
            title='Test event',
            event_date='2028-12-01 00:00',
            created_by=self.user
        )
        self.assertEqual(event.title, 'Test event')
        self.assertEqual(event.project, self.project)

    def test_schedule_meets(self):
        meeting = ScheduleMeet.objects.create(
            project=self.project,
            title='Test meeting',
            description='Test description',
            meeting_date='2028-12-01',
            start_time='2028-12-01 12:00',
            end_time='2028-12-01 12:30',
            location='Test location',
        )
        meeting.participants.add(self.user)
        self.assertEqual(meeting.title, 'Test meeting')
        self.assertTrue(meeting.participants.filter(id=self.user.id).exists())
        