# Generated by Django 3.2.19 on 2024-04-19 19:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news_api', '0002_alter_author_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='password',
        ),
        migrations.RemoveField(
            model_name='author',
            name='username',
        ),
        migrations.AddField(
            model_name='author',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]