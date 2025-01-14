# Generated by Django 4.2.9 on 2024-01-19 04:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(blank=True, max_length=15, null=True)),
                ('user_agent', models.TextField(blank=True)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('is_login', models.BooleanField(blank=True, default=True, null=True)),
                ('is_logged_in', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='login_histories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Login History',
                'verbose_name_plural': 'Login Histories',
                'ordering': ['-date_time'],
            },
        ),
    ]
