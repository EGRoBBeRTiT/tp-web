# Generated by Django 4.1.3 on 2023-11-15 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_profile_managers_questionlike_answerlike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='question',
            name='likes',
        ),
    ]
