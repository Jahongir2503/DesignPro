# Generated by Django 4.2.6 on 2023-11-05 20:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 5, 20, 35, 51, 783800, tzinfo=datetime.timezone.utc)),
        ),
    ]
