# Generated by Django 4.1.7 on 2023-04-10 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_feedback_assessor_score_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='context',
            field=models.TextField(blank=True, max_length=16384, null=True),
        ),
    ]
