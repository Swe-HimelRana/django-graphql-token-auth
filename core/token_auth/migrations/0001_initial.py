# Generated by Django 4.1.3 on 2022-11-08 22:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenAuth',
            fields=[
                ('id', models.CharField(default=uuid.UUID('9df3d9f9-77f8-46d9-b27a-bfc5a07d9b9f'), editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('token', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tokenauth', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceInfo',
            fields=[
                ('id', models.CharField(default=uuid.UUID('40cb9f6e-8a68-4569-af30-893cdab59539'), editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('device_hash', models.CharField(blank=True, max_length=255, null=True)),
                ('device_ip', models.CharField(blank=True, max_length=50, null=True)),
                ('device_user_agent', models.TextField(default='')),
                ('device_language', models.TextField(blank=True, max_length=50, null=True)),
                ('device_accept_encoding', models.TextField(blank=True, max_length=50, null=True)),
                ('device_type', models.TextField(blank=True, max_length=50, null=True)),
                ('device_name', models.TextField(blank=True, max_length=50, null=True)),
                ('device_version', models.TextField(blank=True, max_length=50, null=True)),
                ('device_country', models.TextField(blank=True, max_length=50, null=True)),
                ('device_state', models.TextField(blank=True, max_length=50, null=True)),
                ('device_city', models.TextField(blank=True, max_length=50, null=True)),
                ('device_zip', models.TextField(blank=True, max_length=50, null=True)),
                ('auth_token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device', to='token_auth.tokenauth')),
            ],
        ),
    ]
