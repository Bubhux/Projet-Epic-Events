# Generated by Django 4.2.7 on 2023-12-29 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(blank=True, max_length=255)),
                ('client_name', models.CharField(blank=True, max_length=255)),
                ('client_contact', models.CharField(blank=True, max_length=255)),
                ('event_date_start', models.DateTimeField(blank=True, null=True)),
                ('event_date_end', models.DateTimeField(blank=True, null=True)),
                ('location', models.TextField(blank=True)),
                ('attendees', models.PositiveIntegerField(default=0)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
    ]