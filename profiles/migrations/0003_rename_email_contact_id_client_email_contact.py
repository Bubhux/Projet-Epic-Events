# Generated by Django 4.2.7 on 2023-12-17 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_client_user_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='email_contact_id',
            new_name='email_contact',
        ),
    ]
