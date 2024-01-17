# Generated by Django 4.2.7 on 2023-11-30 08:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_alter_client_user_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='user_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client_profiles', related_query_name='client_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
