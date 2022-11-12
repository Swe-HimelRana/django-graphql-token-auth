# Generated by Django 4.1.3 on 2022-11-09 21:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(default=uuid.UUID('4586713e-0780-459d-a9db-1cd5ae0cc321'), editable=False, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]