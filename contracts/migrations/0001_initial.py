# Generated by Django 4.2.7 on 2023-12-14 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('status_contract', models.BooleanField(default=False, verbose_name='Contract signed')),
                ('total_amount', models.FloatField(default=0.0)),
                ('remaining_amount', models.FloatField(default=0.0)),
            ],
        ),
    ]
