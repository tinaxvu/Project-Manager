# Generated by Django 4.2.16 on 2024-11-14 15:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='assigned_to',
            field=models.ManyToManyField(blank=True, related_name='assigned_todos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='todo',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_todos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='todo',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todos', to='projects.project'),
        ),
        migrations.AddField(
            model_name='timeline',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timeline', to='projects.project'),
        ),
        migrations.AddField(
            model_name='teamhandbook',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_handbook', to='projects.project'),
        ),
        migrations.AddField(
            model_name='tag',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='projects.project'),
        ),
        migrations.AddField(
            model_name='schedulemeet',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_meets', to='projects.project'),
        ),
        migrations.AddField(
            model_name='project',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(related_name='member_projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='requested',
            field=models.ManyToManyField(blank=True, related_name='projects_requested_by_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fileupload',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='projects.project'),
        ),
        migrations.AddField(
            model_name='fileupload',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='files', to='projects.tag'),
        ),
        migrations.AddField(
            model_name='fileupload',
            name='uploaded_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uploaded_files', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='collaboration',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_collaborations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='collaboration',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collaborations', to='projects.project'),
        ),
        migrations.AddField(
            model_name='calendar',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_calendar_events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='calendar',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calendar_events', to='projects.project'),
        ),
    ]
