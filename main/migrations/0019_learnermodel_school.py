# Generated by Django 4.1.7 on 2023-07-03 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_video_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='learnermodel',
            name='school',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
