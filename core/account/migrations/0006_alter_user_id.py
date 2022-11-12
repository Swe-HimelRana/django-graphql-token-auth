# Generated by Django 4.1.3 on 2022-11-09 21:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(default=uuid.UUID('ccec7634-eff8-4e35-a268-2ad1c610a630'), editable=False, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
