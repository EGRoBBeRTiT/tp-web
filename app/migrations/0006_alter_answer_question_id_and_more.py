# Generated by Django 4.1.3 on 2023-11-16 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_delete_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='app.question'),
        ),
        migrations.AlterUniqueTogether(
            name='answerlike',
            unique_together={('profile_id', 'answer_id')},
        ),
        migrations.AlterUniqueTogether(
            name='questionlike',
            unique_together={('profile_id', 'question_id')},
        ),
    ]
