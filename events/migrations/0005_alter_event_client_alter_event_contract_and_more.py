# Generated by Django 4.2.7 on 2023-12-15 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0002_alter_client_user_contact'),
        ('contracts', '0002_initial'),
        ('events', '0004_alter_event_support_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client_events', to='profiles.client', verbose_name='Client'),
        ),
        migrations.AlterField(
            model_name='event',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contract_events', to='contracts.contract', verbose_name='Contract'),
        ),
        migrations.AlterField(
            model_name='event',
            name='support_contact',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 'Support team'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='support_events', to=settings.AUTH_USER_MODEL, verbose_name='Support Contact'),
        ),
    ]
