# Generated by Django 4.1.7 on 2023-03-12 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_rename_list_of_video_ids_recommendationqueue_list_of_module_ids'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='learnermodel',
            name='feedback',
        ),
        migrations.RemoveField(
            model_name='learnermodel',
            name='feedback_edit_history',
        ),
        migrations.RemoveField(
            model_name='learnermodel',
            name='human_approved',
        ),
        migrations.RemoveField(
            model_name='learnermodel',
            name='human_edited',
        ),
        migrations.AddField(
            model_name='module',
            name='feedback',
            field=models.CharField(blank=True, max_length=4096, null=True),
        ),
        migrations.AddField(
            model_name='module',
            name='feedback_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='video',
            name='description',
            field=models.CharField(default='', max_length=4096),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField(blank=True, max_length=4096, null=True)),
                ('human_approved', models.BooleanField(default=False)),
                ('human_edited', models.BooleanField(default=False)),
                ('planner_score', models.FloatField(default=0.0)),
                ('guardian_score', models.FloatField(default=0.0)),
                ('mentor_score', models.FloatField(default=0.0)),
                ('motivator_score', models.FloatField(default=0.0)),
                ('assessor_score', models.FloatField(default=0.0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='learnermodel',
            name='current_feedback',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.feedback'),
        ),
    ]
