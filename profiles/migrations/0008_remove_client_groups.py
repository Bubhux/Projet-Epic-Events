# Generated by Django 4.2.7 on 2023-11-30 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_client_groups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='groups',
        ),
    ]
