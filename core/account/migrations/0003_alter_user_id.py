# Generated by Django 4.1.3 on 2022-11-06 20:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_is_email_verified_user_is_identity_verified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(default=uuid.UUID('3a3b5b43-5ff2-4ee7-9897-467aa4680d9e'), editable=False, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
