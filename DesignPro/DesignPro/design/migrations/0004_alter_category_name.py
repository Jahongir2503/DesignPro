# Generated by Django 4.2.6 on 2023-11-07 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0003_remove_request_due_date_alter_request_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]